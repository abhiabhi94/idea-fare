from django.urls import path
from django.views.generic import TemplateView

from flag.views import flag

app_name = 'flag'

urlpatterns = [
    path('', flag, name='flag'),
]
