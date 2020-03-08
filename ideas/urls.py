from django.contrib import admin
from django.urls import path, re_path
from ideas import views

app_name = 'ideas'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('idea/<slug:slug>',
         views.IdeaDetailView.as_view(), name='idea-details')
]
