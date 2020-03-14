from django.shortcuts import render, redirect
from django.contrib import messages
from meta.views import Meta
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from users.forms import UserRegisterForm, UserUpdateForm
from users.manager import log_in_user

global meta_home
meta_home = Meta(title='IdeaFare | Let us make the world a better place!',
                 description='Read, share and discuss about the ideas that you think can change the world.',
                 keywords=[
                     'idea', 'share', 'innovate',
                     'change', 'discuss', 'curiousity'
                 ])


@require_http_methods(['GET', 'POST'])
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
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account created for {username}. You will now be able to Log In!')
            log_in_user(request, user)
            return redirect('ideas:home')

    else:  # On GET request return a new form
        context['form'] = UserRegisterForm()

    context['meta'] = Meta(title=f'Register | IdeaFare',
                           description=f'Register on IdeaFare',
                           keywords=meta_home.keywords + ['register'])
    return render(request, template_name, context=context)


@require_http_methods(['GET', 'POST'])
@login_required
def profile(request):
    """Allow users to view and update their personal information"""
    template_name = 'users/profile.html'
    if(request.method == 'POST'):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your profile has been updated!')
            # return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form
    }
    context['meta'] = Meta(title=f'Profile | IdeaFrame',
                           description=f'Profile of {request.user.get_full_name().title()} on IdeaFrame',
                           )
    return render(request, template_name, context=context)


@require_http_methods(['GET', 'POST'])
@login_required
def password_change(request):
    """Change users password and log them back in"""
    template_name = 'users/profile.html'
    if(request.method == 'POST'):
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, 'Password updated. You have now be logged out of all other sessions')
            log_in_user(request, user)
            return redirect('ideas:home')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {
        'form': form
    }
    context['meta'] = Meta(title=f'Change Password | IdeaFrame',
                           description=f"""Password change for {request.user.get_full_name().title()}
                            on IdeaFrame""",
                           )
    return render(request, template_name, context=context)
