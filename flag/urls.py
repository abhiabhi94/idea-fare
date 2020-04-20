from django.urls import path
from django.views.generic import TemplateView

from flag.views import flag

app_name = 'flag'

urlpatterns = [
    path('', flag, name='flag'),
    path('thank-you', TemplateView.as_view(template_name='flag/thank_you.html'), name='flag-reported')
]


