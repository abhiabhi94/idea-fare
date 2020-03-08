from django.shortcuts import render
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    ListView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.contrib.syndication.views import Feed
from ideas.models import Idea

global paginate_by
paginate_by = 10


@method_decorator(require_http_methods(['GET']), name='dispatch')
class Home(ListView):
    """Returns the latest ideas created with visibility public"""
    template_name = 'ideas/home.html'
    context_object_name = 'ideas'
    queryset = Idea.objects.filter(visibility=True).all()
    paginate_by


class IdeaDetailView(UserPassesTestMixin, DetailView):
    template_name = 'idea/idea-details.html'
    context_object_name = 'idea'
    queryset = Idea.objects.filter()

    def test_func(self):
        """Allow only creater to view their idea if it's private"""
        idea = self.kwargs.get('slug')
        if not idea.visibility:
            return self.request.user == idea.conceiver.username
        return True
