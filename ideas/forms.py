from django import forms
from django.utils.translation import gettext_lazy as _

from fluent_comments.forms import FluentCommentForm
from fluent_comments.models import FluentComment

from ideas.manager import email_verification


class CommentForm(FluentCommentForm):
    """Adds email verification to django_fluent_comments"""

    class Meta:
        model = FluentComment
        fields = ['name', 'email', 'comment']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        """
        Returns
            email address for valid email
            error message in case of invalid email for unauthenticated users.

        TODO
            No such check is required for authenticated users,\
            this operation has already been performed during\
            signup.Since this would require accessing the\
            WSGIRequest object inside the form, it would mean\
            there needs to be an override somewhere inside the\
            view used for rendering this form. It seems too\
            much work right now, but maybe not in the future.
        """
        email = self.cleaned_data.get('email').lower()
        if not email_verification(email):
            raise forms.ValidationError(
                _('Are you sure %(email)s is a valid email address? We suspect you made a typing error'),
                code='invalid',
                params={'email': email})

        return email
