from collections import namedtuple

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from flag.managers import FlagInstanceManager, FlagManager

User = get_user_model()


class Flag(models.Model):
    """Used to add flag/moderation to a model"""
    class State(models.IntegerChoices):
        UNFLAGGED = 1
        FLAGGED = 2, _('Flagged')
        REJECTED = 3, _('Flag rejected by moderator')
        NOTIFIED = 4, _('Creator notified')
        RESOLVED = 5, _('Content modified or deleted')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    creator = models.ForeignKey(User, related_name='flags_against', null=True, on_delete=models.CASCADE)
    state = models.SmallIntegerField(choices=State.choices, default=State.UNFLAGGED)
    moderator = models.ForeignKey(User, null=True, related_name='flags_moderated', on_delete=models.SET_NULL)
    count = models.PositiveIntegerField(default=0)

    objects = FlagManager()

    class Meta:
        verbose_name = _('Flag')
        unique_together = ['content_type', 'object_id']

    def increase_count(self):
        field = 'count'
        self.refresh_from_db()
        self.count = models.F(field) + 1
        self.save(update_fields=[field])

    def decrease_count(self):
        field = 'count'
        self.refresh_from_db()
        self.count = models.F(field) - 1
        self.save(update_fields=[field])

    def toggle_state(self):
        allowed_flags = getattr(settings, 'FLAGS_ALLOWED', 0)
        self.refresh_from_db()
        field = 'state'
        if self.count > allowed_flags and getattr(self, field) == self.State.UNFLAGGED:
            setattr(self, field, self.State.FLAGGED)
        else:
            setattr(self, field, self.State.UNFLAGGED)
        self.save(update_fields=[field])


class FlagInstance(models.Model):
    REASON = getattr(settings, "FLAG_REASONS", [
        (1, _("Spam | Exists only to promote a service ")),
        (2, _("Abusive | Intended at promoting hatred")),
    ])

    REASON.append((100, _('Something else')))

    # Make a named tuple
    Reasons = namedtuple('Reason', ['value', 'reason'])

    # Construct the list of named tuples
    reasons = []
    for reason in REASON:
        reasons.append(Reasons(*reason))

    reason_values = [reason.value for reason in reasons]

    flag = models.ForeignKey(Flag, related_name='flags', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='flags_by', on_delete=models.CASCADE)
    date_flagged = models.DateTimeField(auto_now_add=timezone.now)
    reason = models.SmallIntegerField(choices=REASON, default=reason_values[0])
    info = models.TextField(null=True, blank=True)

    objects = FlagInstanceManager()

    class Meta:
        verbose_name = _('Flag Instance')
        verbose_name_plural = _('Flag Instances')
        unique_together = ['flag', 'user']
        ordering = ['-date_flagged']

    def clean(self):
        """If something else is choosen, info shall not be empty"""
        if self.reason == self.reason_values[-1] and not self.info:
            raise ValidationError(
                {
                    'info': ValidationError(
                        _('Please provide some information why you choose to report the content'),
                        code='required')
                }
            )

    def save(self, *args, **kwargs):
        self.clean()
        super(FlagInstance, self).save(*args, **kwargs)


@receiver(post_save, sender=FlagInstance)
def flagged(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        instance.flag.increase_count()
        instance.flag.toggle_state()


@receiver(post_delete, sender=FlagInstance)
def unflagged(sender, instance, using, **kwargs):
    """Decrease flag count in the flag model before deleting an instance"""
    instance.flag.decrease_count()
    instance.flag.toggle_state()
