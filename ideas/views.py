from django.shortcuts import render
from django.views.generic import (CreateView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView,
                                  ListView
                                  )
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import HttpResponseBadRequest, JsonResponse
from meta.views import Meta
from ideas.models import Idea
from ideas.manager import (email_verification,
                           get_public_ideas,
                           process_idea_form
                           )
from subscribers.models import Subscriber

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
        email = request.POST['email']
        data['email'] = email
        if email_verification(email):
            try:
                Subscriber.objects.create(email=email)
                data['msg'] = ' is now registered successfully with us'
                data['status'] = 0
            except IntegrityError:
                data['msg'] = ' is already registered with us'
            except:
                data['status'] = 1
                data['msg'] = 'There seems to be an issue on our side. Please retry.'
            return JsonResponse(data)

        data['msg'] = ' is not a valid email'
        return JsonResponse(data)
    return HttpResponseBadRequest


@require_http_methods(['GET'])
def about(request):
    """Returns information about the concept of IdeaFare"""
    context = {}
    context['meta'] = Meta(title=f'About | IdeaFare',
                           description=f'Know a bit about the concept and the idea behind the IdeaFare',
                           keywords=meta_home.keywords + ['about'])
    template_name = 'ideas/about.html'
    return render(request, template_name, context)


@require_http_methods(['GET'])
def content_policy(request):
    """Returns information about the content policy of IdeaFare"""
    context = {}
    context['meta'] = Meta(title=f'Content Policy | IdeaFare',
                           description=f'Content Policy for adding content on IdeaFare',
                           keywords=meta_home.keywords + ['content policy'])
    template_name = 'ideas/content_policy.html'
    return render(request, template_name, context)


@require_http_methods(['GET'])
def privacy_policy(request):
    """Returns information about the privacy policy of IdeaFare"""
    context = {}
    context['meta'] = Meta(title=f'Privacy Policy | IdeaFare',
                           description=f'Privacy Policy by IdeaFare',
                           keywords=meta_home.keywords + ['privacy policy'])
    template_name = 'ideas/privacy_policy.html'
    return render(request, template_name, context)


@method_decorator(require_http_methods(['GET']), name='dispatch')
class Home(ListView):
    """Returns the latest ideas created with visibility public"""
    template_name = 'ideas/home.html'
    context_object_name = 'ideas'
    queryset = Idea.objects.filter(visibility=True).all()
    paginate_by

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['meta'] = meta_home
        return context


@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
class IdeaCreateView(CreateView):
    template_name = 'ideas/idea_form.html'
    context_object_name = 'idea'
    model = Idea
    fields = ['title', 'concept', 'visibility',
              #   'tags'
              ]

    def form_invalid(self, form):
        """For a valid form, check if the user wants the idea to be anonymous."""

        form = process_idea_form(request, form)


@method_decorator(require_http_methods(['GET']), name='dispatch')
class IdeaDetailView(UserPassesTestMixin, DetailView):
    """Returns detail view for an idea if it is public or is owned by the logged in user"""
    template_name = 'ideas/idea_details.html'
    context_object_name = 'idea'
    queryset = Idea.objects.filter()

    def test_func(self):
        """Allow only conceiver to view their idea if it's private"""
        idea = self.get_object()
        if not idea.visibility:
            return self.request.user == idea.conceiver
        return True


@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
class IdeaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Idea
    fields = ['title', 'concept', 'visibility'
              #   'tags',
              ]

    def form_valid(self, form):
        """Check whether the user logged in is the one updating the idea."""
        idea = self.get_object()
        if self.request.user == idea.conceiver:
            form = process_idea_form(self.request, form)
            messages.success(
                self.request, 'Your idea has been successfully updated.')
        else:
            messages.warning(
                self.request, 'You are not allowed to tinker with this idea.')
            return redirect('idea:home')

        return super().form_valid(form)

    def test_func(self):
        """ensuring the conceiver themselves is updating their idea"""
        idea = self.get_object()
        if self.request.user == idea.conceiver:
            return True
        raise PermissionDenied('You are not allowed to update this request')


@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
class IdeaDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Idea
    fields = ['title', 'concept', 'visibility'
              # 'tags'
              ]
    context_object_name = 'idea'
    success_url = reverse_lazy('ideas:home')
    success_message = 'Idea {} was removed successfully'

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
    model = Idea
    template_name = 'ideas/conceiver_ideas.html'
    queryset = Idea.objects.all()
    context_object_name = 'ideas'
    paginate_by

    def get_queryset(self):
        username = self.kwargs.get('username', None)
        # Return anonymous posts
        if username is not None and username == 'anonymous':
            return self.queryset.filter(user=None)

        user = get_object_or_404(User, username=username)
        if self.request.user == user:
            return self.queryset.filter(user=user)

        # Show only public posts
        return get_public_ideas().filter(user=user)

    def get_context_data(self, **kwargs):
        context = super(ConceiverIdeaListView, self).get_context_data(**kwargs)
        username = self.kwargs.get('username', None)

        # Return anonymous posts
        if username is not None and username == 'anonymous':
            user = AnonymousUser
            name = user
        else:
            user = get_object_or_404(User, username=username)
            name = user.get_full_name()

        context['meta'] = Meta(title=f'{name} | Idea',
                               description=f'Ideas authored by {name}',
                               og_author=f'{name}',
                               keywords=meta_home.keywords)
        return context


class LatestPostRSSFeed(Feed):
    title = 'Latest ideas from IdeaFare'
    link = ''
    description = meta_home.description

    # def feed_extra_kwargs(self, obj):
    #     return {}

    def items(self, top_n=5):
        return get_public_ideas()[:top_n]

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
