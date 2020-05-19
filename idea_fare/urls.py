from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

import debug_toolbar

from utils.decorators import require_superuser
from users import views as user_views

def dec_patterns(patterns):
    decorated_patterns = []
    for pattern in patterns:
        callback = pattern.callback
        pattern.callback = require_superuser(callback)
        pattern._callback = require_superuser(callback)
        decorated_patterns.append(pattern)
    return decorated_patterns

urlpatterns = [
    path('admin/', (dec_patterns(admin.site.urls[0]),) + admin.site.urls[1:]),
]

urlpatterns += [
    path('', include('ideas.urls')),
    path('idea/comments/', include('fluent_comments.urls')),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(
        redirect_authenticated_user=True,
        template_name='users/login.html'),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='users/logout.html'),
        name='logout'
    ),
    path('password-change/', user_views.password_change, name='password-change'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'),
         name='password_reset'
         ),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'),
         name='password_reset_done'
         ),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'
         ),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'),
         name='password_reset_complete'
         ),
    path('flag', include('flag.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    urlpatterns += [path('__debug__', include(debug_toolbar.urls))]
