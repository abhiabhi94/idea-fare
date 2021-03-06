from dal import autocomplete
from django.forms import ModelForm, Textarea
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from ideas.models import Idea


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
