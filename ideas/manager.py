"""
Module contains functions that will be re-usable inside applications.
Ideally, the logical part (apart from that written in models) in views should be placed here.
"""
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from validate_email import validate_email
from ideas.models import Idea


def process_idea_form(request, form):
    """
    Returns
        form: obj
            The processed form
    Args
        request: WSGIRequest
            The incoming request object

        form: IdeaForm
            The form to be processed
    """
    if not (request.POST.get('anonymous', True) == 'anonymous'):  # Non-anonymous ideas
        if request.user.is_authenticated:
            # For authenticated users
            form.instance.user = request.user
    else:  # Anonymous ideas can't be made private
        form.instance.visibility = True

    return form


def get_public_ideas(order='-date_created'):
    """
    Returns
        QuerySet
            the set of ideas that are public

    Args
        order: str
            The field according to which the list will be sorted
    """
    return Idea.objects.filter(visibility=True).order_by(order)


def email_verification(email):
    """Verify whether an email is legit or not"""
    return validate_email(email_address=email, check_regex=True, check_mx=True)


def latest_entry(request):
    """
    Returns
        date: date-time
            The date of the latest public idea posted.
    """
    return Idea.objects.filter(visibility=True).latest('-date_created').date_created
