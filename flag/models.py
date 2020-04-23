from collections import namedtuple
from enum import IntEnum

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from flag import signals

STATUS = getattr(settings, "FLAG_STATUSES", [
    (1, _("flagged")),
    (2, _("flag rejected by moderator")),
    (3, _("creator notified")),
    (4, _("content removed by creator")),
    (5, _("content removed by moderator")),
])

REASON = getattr(settings, "FLAG_REASONS", [
    (1, _("Spam | Exists only to promote a service ")),
    (2, _("Abusive | Intended at promoting hatred")),
    (3, _("Something Else")),
])

# Make a named tuple
reasons = namedtuple('reasons', ['value', 'reason'])

# Construct the list of named tuples
reasons = [reasons(*reason) for reason in REASON]
reason_values = [reason.value for reason in reasons]

class FlaggedContent(models.Model):
    """Used to add flag/moderation to a model"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    creator = models.ForeignKey(User, related_name='flagged_content_creator', null=True, on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=STATUS, default=1)
    moderator = models.ForeignKey(User, null=True, related_name='moderated_content', on_delete=models.SET_NULL)
    count = models.SmallIntegerField(default=1)

    class Meta:
        unique_together = ['content_type', 'object_id']


class FlagInstance(models.Model):

    flagged_content = models.ForeignKey(FlaggedContent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='flagger', null=True, on_delete=models.SET_NULL)
    date_flagged = models.DateTimeField(auto_now_add=timezone.now)
    reason = models.SmallIntegerField(choices=REASON, default=reason_values[0])
    comment = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ['flagged_content', 'user']
        ordering = ['-date_flagged']

    def clean(self):
        """If the last reason is choosen, comment shall not be empty"""
        if self.reason == reason_values[-1] and not self.comment:
            raise ValidationError(
                {
                    'comment': ValidationError(_("Please provide some information why you choose to report the content"),code='required')
                }
            )

    def save(self, *args, **kwargs):
        self.clean()
        super(FlagInstance, self).save(*args, **kwargs)


def add_flag(flagger, content_type, object_id, content_creator, reason, comment=None, status=None):
    """
    Flag contents related to a model for moderation and return the instance

    Parameters
    ----------
    flagger : User
        User flagging the content
    content_type : ContentType
        The ContentType framework
    object_id : int
        The id of the model instance to be flagged
    content_creator : User
        The creator of the model instance that needs to be flagged
    reason: int
        The reason for flagging. A mapping to the `REASON`
    comment : str, optional
        Comment if any stating the reason for the flag, by default None
    status : int, optional
        The status of the flag, by default None
    """

    defaults = {}
    if content_creator.pk is not None: # anonymous user # don't match username as username might be 'anonymous'
        defaults["creator"] = content_creator
    if status is not None:
        defaults['status'] = status

    flagged_content, created = FlaggedContent.objects.get_or_create(
        content_type=content_type,
        object_id=object_id,
        **defaults
    )

    if not created:
        flagged_content.count = models.F('count') + 1
        flagged_content.save()
        flagged_content.refresh_from_db()

    flag_instance = FlagInstance(
        flagged_content=flagged_content,
        user=flagger,
        reason=reason,
        comment=comment
    )
    flag_instance.save()


    signals.content_flagged.send(
        sender=FlaggedContent,
        flagged_content=flagged_content,
        flag_instance=flag_instance,
        reason=reason,
        comment=comment
    )

    return flag_instance
