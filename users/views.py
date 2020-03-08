from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from meta.views import Meta
from django.views.decorators.http import require_http_methods
from users.forms import UserRegisterForm, UserUpdateForm

global meta_home
meta_home = Meta(title='IdeaFare | Let us make the world a better place!',
                 description='Read, share and discuss about the ideas that you think can change the world.',
                 keywords=[
                     'idea', 'share', 'innovate',
                     'change', 'discuss', 'curiousity'
                 ])


@require_http_methods(['GET'])
def register(request):
    # Redirect to the homepage in case user is logged in.
    if request.user.is_authenticated:
        messages.warning(
            request, 'You are already logged in!'
        )
        return redirect('ideas:home')

    template_name = 'Users/register.html'
    context = {}
    if(request.method == 'POST'):
        context['form'] = form = UserRegisterForm(request.POST)
        if(form.is_valid()):
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account created for {username}. You will now be able to Log In!')
            return redirect('ideas:home')
    else:  # On GET request return a new form
        context['form'] = UserRegisterForm()

    context['meta'] = Meta(title=f'Register | IdeaFare',
                           description=f'Register on IdeaFare',
                           keywords=meta_home.keywords + ['register'])
    return render(request, template_name, context)


@require_http_methods(['GET'])
def privacy_policy(request):
    context = {}
    template_name = 'idea/privacy_policy.html'
    context['meta'] = Meta(title=f'Privacy Policy | IdeaFare',
                           description=f"IdeaFare's privacy policy",
                           keywords=meta_home.keywords + ['privacy policy'])
    return render(request, template_name, context)
