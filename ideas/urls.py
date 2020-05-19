from django.urls import path
from django.views.decorators.http import condition

from ideas import views
from ideas.utils import latest_entry

app_name = 'ideas'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('content-policy/', views.content_policy, name='content-policy'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('idea/new/', views.NonAnonymousIdeaCreateView.as_view(),
         name='idea-create-non-anonymous'),
    path('idea/anonymous/new/',
         views.AnonymousIdeaCreateView.as_view(), name='idea-create-anonymous'),
    path('idea/<slug:slug>/',
         views.IdeaDetailView.as_view(), name='idea-details'),
    path('idea/<slug:slug>/update/',
         views.IdeaUpdateView.as_view(), name='idea-update'),
    path('idea/<slug:slug>/delete/',
         views.IdeaDeleteView.as_view(), name='idea-delete'),
    path('idea/conceiver/<str:username>/',
         views.ConceiverIdeaListView.as_view(), name='conceiver-ideas'),
    path('idea/tag/<slug:slug>', views.TaggedIdeaListView.as_view(), name='tagged'),
    path('subscription/', views.subscribe, name='subscription'),
    path('latest/rss-feed/',
         condition(last_modified_func=latest_entry)(views.LatestIdeaRSSFeed()),
         name='rss-feed'),
    path('tags-autocomplete/',
        views.TagsAutoComplete.as_view(),
        name='tags-autocomplete',
    ),
]
