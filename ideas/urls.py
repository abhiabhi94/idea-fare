from django.contrib import admin
from django.urls import path
from ideas import views

app_name = 'ideas'

urlpatterns = [
    path('', views.home, name='home')
]
