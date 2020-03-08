from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings
import debug_toolbar
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', include('ideas.urls')),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        redirect_authenticated_user=True,
        template_name='Users/login.html'),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='Users/logout.html'),
        name='logout'
    ),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='Users/password_reset.html'),
         name='password_reset'
         ),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='Users/password_reset_done.html'),
         name='password_reset_done'
         ),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='Users/password_reset_confirm.html'),
         name='password_reset_confirm'
         ),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='Users/password_reset_complete.html'),
         name='password_reset_complete'
         ),
    # path('latest/feed',
    #      condition(last_modified_func=latest_entry)(rss_feed()),
    #      name='rss-feed'
    #      ),
    path('privacy-policy', user_views.privacy_policy, name='privacy-policy'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    urlpatterns += [path('__debug__', include(debug_toolbar.urls))]
