from enum import IntEnum

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings
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

class FlaggedContent(models.Model):
    """Used to add flag/moderation to a model"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    creater = models.ForeignKey(User, related_name='flagged_content', on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=STATUS, default=1)
    moderator = models.ForeignKey(User, null=True, related_name='moderated_content', on_delete=models.SET_NULL)
    count = models.SmallIntegerField(default=1)

    class Meta:
        unique_together = ['content_type', 'object_id']

class FlagInstance(models.Model):

    flagged_content = models.ForeignKey(FlaggedContent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='flagger', null=True, on_delete=models.SET_NULL)
    date_flagged = models.DateTimeField(auto_now_add=timezone.now)
    comment = models.TextField(null=True, blank=True)

def add_flag(flagger, content_type, object_id, content_creator, comment=None, status=None):
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
    comment : str, optional
        Comment if any stating the reason for the flag, by default None
    status : int, optional
        The status of the flag, by default None
    """
    defaults = dict(creator=content_creator)
    if status is not None:
        defaults['status'] = status
    if comment is not None:
        defaults['comment'] = comment
    
    flagged_content, created = FlaggedContent.objects.get_or_create(
        content_type=content_type,
        object_id = object_id,
        **defaults
    )

    if not created:
        flagged_content.count = models.F('count') + 1
        flagged_content.save()
        flagged_content.refresh_from_db()

    flag_instance = FlagInstance(
        flagged_content=flagged_content,
        user=flagger,
        comment=comment
    )
    flag_instance.save()
    
    signals.content_flagged.send(
        sender=FlaggedContent,
        flagged_content=flagged_content,
        flag_instance=flag_instance
    )

    return flag_instance
