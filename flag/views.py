from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.html import escape
from django.views.decorators.http import require_POST

from flag.models import add_flag

@login_required
@require_POST
def flag(request):
    """
    Flag an instance
    
    Parameters
    ----------
    request : WSGI object
        [description]
    """
    # if not request.is_ajax():
    #     return HttpResponseBadRequest('Expecting AJAX call')

    data = request.POST.copy()

    # Look up for the instance to be flagged
    ctype = data.get('content_type', None)
    object_id = data.get('object_id', None)
    creator_field = data.get('creator_field', None)
    next_link = data.get('next_link', None)
    if ctype is None or object_id is None:
        return HttpResponseBadRequest('Missing content_type or object_id field')

        except ValueError:
        return HttpResponseBadRequest("Invalid object_pk value: {0}".format(escape(object_id)))
    except (TypeError, LookupError):
        return HttpResponseBadRequest("Invalid content_type value: {0}".format(escape(ctype)))
    except AttributeError:
        return HttpResponseBadRequest("The given content-type {0} does not resolve to a valid model.".format(escape(ctype)))
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("No object matching content-type {0} and object ID {1} exists.".format(escape(ctype), escape(object_id)))
    except (ValueError, ValidationError) as e:
        return HttpResponseBadRequest("Attempting go get content-type {0!r} and object ID {1!r} exists raised {2}".format(escape(ctype), escape(object_id), e.__class__.__name__))

    content_type = get_object_or_404(ContentType, id=int(ctype))
    object_id = int(object_id)

    content_object = content_type.get_object_for_this_type(id=object_id)
    
    if creator_field and hasattr(content_object, creator_field):
        creator = getattr(content_object, creator_field)
    else:
        creator = None

    add_flag(require.user, content_type, object_id, creator, comment)

    messages.success(request, _("You have added a flag. A moderator will review your submission "
                                "shortly."), fail_silently=True)

    if next_link:
        return HttpResponseRedirect(next_link)
    else:
        return HttpResponseRedirect(reverse_lazy('flag-reported'))