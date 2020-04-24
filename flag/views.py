from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms import forms
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.html import escape
from django.views.decorators.http import require_POST

from flag.exceptions import FlagBadRequest
from flag.models import add_flag, reason_values

def clean_reason(reason):
    """
    Clean and return the value of reason
    Raises 404 error if the value is not one among `reason_values`

    Args:
        reason (char): The reason attribute to be cleaned

    Returns:
        char: cleaned value
    """
    err_msg_reason = 'Invalid reason value: {0}'.format(escape(reason))
    try:
        reason = int(reason)
    except TypeError:
        FlagBadRequest(err_msg_reason)

    if not reason or reason not in reason_values:
        FlagBadRequest(err_msg_reason)
    return reason

def user_has_reported_this_content_earlier(request, content_object):
    """
    Returns boolean information about whether the content object has been\
    reported by the current user or not.
    If this happens to be true, an warning is also send using the `messgaes` module.

    Args:
        request (WSGI Request object)
        content_object (ContentType): The object to be verified

    Returns:
        bool
    """

    if content_object.flag.filter(flaginstance__user=request.user).exists():
        messages.warning(request, _('You have already reported this content. Please wait while a moderator reviews your request'))
        return True
    return False


@login_required
@require_POST
def flag(request):
    """
    Flag an instance

    Parameters
    ----------
    request : WSGI object
    """
    data = request.POST.copy()
    # Look up for the instance to be flagged
    ctype = data.get('content_type', None)
    object_id = data.get('object_id', None)
    if ctype is None or object_id is None:
        return FlagBadRequest('Missing content_type or object_id field')

    content_type = get_object_or_404(ContentType, id=int(ctype))

    try:
        object_id = int(object_id)
    except TypeError:
            return FlagBadRequest(_('Invalid object_pk value: {0}'.format(escape(object_id))))

    content_object = content_type.get_object_for_this_type(id=object_id)
    creator_field = data.get('creator_field', None)
    if creator_field and hasattr(content_object, creator_field):
        creator = getattr(content_object, creator_field)
    else:
        creator = None

    reason = data.get('reason', None)
    reason = clean_reason(reason)

    comment = data.get('comment', None)

    if reason == reason_values[-1] and not comment:
        FlagBadRequest('Please provide some information why you choose to report the content')

    if not user_has_reported_this_content_earlier(request, content_object):
        add_flag(request.user, content_type, object_id, creator, reason, comment)

        messages.success(request,
            _('The content has been reported successfully. A moderator will review your submission shortly'),
            fail_silently=True
            )

    next_link = data.get('next_link', None)
    if next_link:
        return HttpResponseRedirect(next_link)
    else:
        return HttpResponseRedirect(reverse_lazy('flag-reported'))
