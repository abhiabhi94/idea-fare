from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from meta.views import Meta
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
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
    """Register a non-logged in user"""
    # Redirect to the homepage in case user is logged in.
    if request.user.is_authenticated:
        messages.warning(
            request, 'You are already logged in!'
        )
        return redirect('ideas:home')

    template_name = 'users/register.html'
    context = {}
    if(request.method == 'POST'):
        context['form'] = form = UserRegisterForm(request.POST)
        if(form.is_valid()):
            form.save()
            username = form.cleaned_data.get('username')
            password = request.POST['password']
            messages.success(
                request, f'Account created for {username}. You will now be able to Log In!')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                messages.info(
                    'Unable to log you in automatically. Please try going through the login page')
            redirect('idea:home')

    else:  # On GET request return a new form
        context['form'] = UserRegisterForm()

    context['meta'] = Meta(title=f'Register | IdeaFare',
                           description=f'Register on IdeaFare',
                           keywords=meta_home.keywords + ['register'])
    return render(request, template_name, context)


@require_http_methods(['GET', 'POST'])
@login_required
def profile(request):
    """Allow users to view and update their personal information"""
    template_name = 'users/profile.html'
    if(request.method == 'POST'):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form,
    }
    context['meta'] = Meta(title=f'Profile | IdeaFrame',
                           description=f'Profile of {request.user.get_full_name().title()} on IdeaFrame',
                           )
    return render(request, template_name, context)


@require_http_methods(['GET'])
def privacy_policy(request):
    context = {}
    template_name = 'Blog/privacy_policy.html'
    context['meta'] = Meta(title=f'Privacy Policy | HackAdda',
                           description=f'Privacy Policy by HackAdda',
                           keywords=meta_home.keywords + ['privacy policy'])
    return render(request, template_name, context)


@require_http_methods(['GET'])
def image_license(request):
    context = {}
    template_name = 'Blog/image_license.html'
    context['meta'] = Meta(title=f'Image License | HackAdda',
                           description=f'Image License by HackAdda',
                           keywords=meta_home.keywords + ['image license'])
    return render(request, template_name, context)
