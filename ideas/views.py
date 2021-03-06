from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.syndication.views import Feed
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from meta.views import Meta
from taggit.models import Tag

from ideas.forms import AnonymousIdeaCreateForm, NonAnonymousIdeaCreateForm
from ideas.models import Idea
from ideas.utils import process_idea_form
from subscribers.models import Subscriber
from utils import validators

global paginate_by
paginate_by = 15

global meta_home
meta_home = Meta(title='IdeaFare | Let us make the world a better place!',
                 description='Read, share and discuss about the ideas that you think can change the world.',
                 keywords=[
                     'idea', 'share', 'innovate',
                     'change', 'discuss', 'curiousity'
                 ])


@require_http_methods(['POST'])
def subscribe(request):
    """
    adds emails to the model Subscribers after verifying legit emails only on POST requests.
    Returns Jsonresponse with properties response and status.
    """
    data = {'msg': '', 'email': '', 'status': -1}
    if request.method == 'POST' and request.is_ajax():
        email = request.POST.get('email', None)
        if email:
            data['email'] = email
            if validators.is_email_valid(email):
                __, created = Subscriber.objects.get_or_create(email=email)
                if created:
                    data['msg'] = _(' is now registered successfully with us')
                    data['status'] = 0
                else:
                    data['msg'] = _(' is already registered with us')

                return JsonResponse(data)

            data['msg'] = _(' is not a valid email')
            return JsonResponse(data)
        return HttpResponseBadRequest(_('Bad Request! email not present'))
    return HttpResponseBadRequest(_('Bad Request!'))


@require_http_methods(['GET'])
def about(request):
    """Returns information about the concept of IdeaFare"""
    context = {}
    context['meta'] = Meta(title='About | IdeaFare',
                           description='Know a bit about the concept and the idea behind the IdeaFare',
                           keywords=meta_home.keywords + ['about'])
    template_name = 'ideas/about.html'
    return render(request, template_name, context)


@require_http_methods(['GET'])
def content_policy(request):
    """Returns information about the content policy of IdeaFare"""
    context = {}
    context['meta'] = Meta(title='Content Policy | IdeaFare',
                           description='Content Policy for adding content on IdeaFare',
                           keywords=meta_home.keywords + ['content policy'])
    template_name = 'ideas/content_policy.html'
    return render(request, template_name, context)


@require_http_methods(['GET'])
def privacy_policy(request):
    """Returns information about the privacy policy of IdeaFare"""
    context = {}
    context['meta'] = Meta(title='Privacy Policy | IdeaFare',
                           description='Privacy Policy by IdeaFare',
                           keywords=meta_home.keywords + ['privacy policy'])
    template_name = 'ideas/privacy_policy.html'
    return render(request, template_name, context)


@method_decorator(require_http_methods(['GET']), name='dispatch')
class Home(ListView):
    """Returns the latest ideas created with visibility public"""
    template_name = 'ideas/home.html'
    context_object_name = 'ideas'
    queryset = Idea.public_objects.all()
    paginate_by = paginate_by

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['meta'] = meta_home
        return context


@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
class AnonymousIdeaCreateView(CreateView):
    """Submit ideas anonymously"""
    form_class = AnonymousIdeaCreateForm
    model = Idea
    template_name = 'ideas/idea_form.html'
    context_object_name = 'idea'

    def form_valid(self, form):
        """For a valid form, check if the user wants the idea to be anonymous."""
        process_idea_form(self.request, form)
        return super().form_valid(form)


@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
class NonAnonymousIdeaCreateView(LoginRequiredMixin, AnonymousIdeaCreateView):
    """Submit ideas non-anonymously"""
    form_class = NonAnonymousIdeaCreateForm


@method_decorator(require_http_methods(['GET']), name='dispatch')
class IdeaDetailView(UserPassesTestMixin, DetailView):
    """Returns detail view for an idea if it is public or is owned by the logged in user"""
    template_name = 'ideas/idea_details.html'
    context_object_name = 'idea'
    queryset = Idea.objects.all()

    def test_func(self):
        """Allow only conceiver to view their idea if it's private"""
        idea = self.get_object()
        if not idea.visibility:
            if self.request.user == idea.conceiver:
                return True
            return PermissionDenied(_('You are not authorised to view this idea.'))
        return True


@method_decorator(require_http_methods(['GET', 'POST', 'PUT']), name='dispatch')
class IdeaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows only conceivers to update their idea"""
    model = Idea
    form_class = NonAnonymousIdeaCreateForm

    def form_valid(self, form):
        """Check whether the user logged in is the one updating the idea."""
        idea = self.get_object()
        if self.request.user == idea.conceiver:
            form = process_idea_form(self.request, form)
            messages.success(
                self.request, _('Your idea has been successfully updated.'))
        else:
            messages.warning(
                self.request, _('You are not allowed to update this idea.'))
            return redirect('idea:home')

        return super().form_valid(form)

    def test_func(self):
        """ensuring the conceiver themselves is updating their idea"""
        idea = self.get_object()
        if idea.user is None:
            raise PermissionDenied(
                _('Idea by anonymous user can not be edited or deleted.'))
        if self.request.user == idea.conceiver:
            return True
        raise PermissionDenied(_('You are not allowed to update this request'))


@method_decorator(require_http_methods(['GET', 'POST', 'DELETE']), name='dispatch')
class IdeaDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """Allow only conceivers to delete their idea and give a successfull message upon completion"""
    model = Idea
    context_object_name = 'idea'
    success_url = reverse_lazy('ideas:home')
    success_message = _('Idea {} was removed successfully')

    def test_func(self):
        """ensuring the conceiver themselves is deleting their idea"""
        return IdeaUpdateView.test_func(self)

    def form_valid(self, form):
        """Validate the form"""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def delete(self, request, *args, **kwargs):
        idea = self.get_object()
        messages.success(self.request, self.success_message.format(idea))
        return super().delete(request, *args, **kwargs)


@method_decorator(require_http_methods(['GET']), name='dispatch')
class ConceiverIdeaListView(ListView):
    """
    Returns the list of all idea by a conceiver(user)
    All anonymous users are considered the same.
    """
    model = Idea
    template_name = 'ideas/conceiver_ideas.html'
    queryset = Idea.objects.all()
    context_object_name = 'ideas'
    paginate_by = paginate_by

    def get_queryset(self):
        username = self.kwargs.get('username', None)
        # Return anonymous posts
        if username is not None and username == 'anonymous':
            return self.queryset.filter(user=None)

        user = get_object_or_404(User, username=username.lower())

        if self.request.user == user:  # For logged in users return all of their ideas
            return self.queryset.filter(user=user)

        # Show only public ideas
        return Idea.public_objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super(ConceiverIdeaListView, self).get_context_data(**kwargs)
        username = self.kwargs.get('username', None)

        # Return anonymous posts
        if username is not None and username == 'anonymous':
            user = AnonymousUser
            name = user
        else:
            user = get_object_or_404(User, username=username.lower())
            name = user.get_full_name()

        context['meta'] = Meta(title=f'{name} | Idea',
                               description=f'Ideas authored by {name}',
                               og_author=f'{name}',
                               keywords=meta_home.keywords)
        return context


@method_decorator(require_http_methods(['GET']), name='dispatch')
class TaggedIdeaListView(ListView):
    template_name = 'ideas/idea_tagged.html'
    context_object_name = 'ideas'

    def get_queryset(self):
        idea_list = Idea.objects.all().filter(
            tags__slug=self.kwargs.get('slug').lower())
        if idea_list:
            return idea_list
        raise Http404('Tag not present')

    paginate_by = paginate_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug').lower()
        tag = get_object_or_404(Tag, slug=slug).name
        context['meta'] = Meta(title='About | IdeaFare',
                               description=f'Ideas with the tag {tag}',
                               keywords=meta_home.keywords + [tag])
        context['tag'] = tag
        return context


@method_decorator(require_http_methods(['GET']), name='dispatch')
class TagsAutoComplete(autocomplete.Select2QuerySetView):
    """Used for autocompletion of tags"""
    def get_queryset(self):

        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs.order_by('name')


class LatestIdeaRSSFeed(Feed):
    """"Publish the RSS feed for latest public ideas"""
    title = _('Latest ideas from IdeaFare')
    link = ''
    description = meta_home.description

    # def feed_extra_kwargs(self, obj):
    #     return {}

    def items(self, top_n=5):
        return Idea.public_objects.all()[:top_n]

    def item_title(self, item):
        return item.title

    def item_author_name(self, item):
        if item.user is None:
            return AnonymousUser()
        return item.conceiver.get_full_name()

    def item_description(self, item):
        return item.concept

    def item_link(self, item):
        return item.get_absolute_url()
