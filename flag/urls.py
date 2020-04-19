from django.urls import path
from django.views.generic import TemplateView

from flag.views import Flag

urlpatterns = [
    path('', Flag.as_view, name='flag'),
    path('thank-you', TemplateView.as_view(template_name='flag/thank_you.html'), name='flag-reported')
]


