from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, Textarea, ValidationError
from fluent_comments.forms import FluentCommentForm
from fluent_comments.models import FluentComment
from dal import autocomplete
from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from ideas.manager import email_verification
from ideas.models import Idea

"""
TODO:
    Both AnonymousIdeaCreateForm and NonAnonymousIdeaCreateForm have\
    a lot of code that is common, only the field inside the Meta class\
    is different. In an ideal world, we would want to have a mixing and\
    use the mixin in both the forms by just overriding the fields.
"""


class AnonymousIdeaCreateForm(ModelForm):
    """Form for anonymous users"""

    captcha = ReCaptchaField() 
    
    class Meta:
        model = Idea
        fields = ['title', 'concept', 'tags', 'captcha']
        widgets = {
            'concept': Textarea(attrs={'col': 80, 'row': 20}),
            'tags': autocomplete.TaggitSelect2('ideas:tags-autocomplete')
        }

class NonAnonymousIdeaCreateForm(autocomplete.FutureModelForm, ModelForm):
    """Form for authenticated users"""

    captcha = ReCaptchaField() 

    class Meta:
        model = Idea
        fields = ['title', 'concept', 'tags', 'visibility', 'captcha']
        widgets = {
            'concept': Textarea(attrs={'col': 80, 'row': 20}),
            'tags': autocomplete.TaggitSelect2('ideas:tags-autocomplete')
        }


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
            raise ValidationError(
                'Are you sure %(email)s is a valid email address? We suspect you made a typing error',
                code='invalid',
                params={'email': email})

        return email
