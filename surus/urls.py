from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.shortcuts import redirect
from apps.api import profile_views


def password_reset_frontend_redirect(request, uidb64, token):
    response = redirect(
        'http://localhost:8080/password_reset/'+uidb64+'/'+token)
    return response


urlpatterns = [
    re_path(r"^password_reset/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$",
            password_reset_frontend_redirect,
            name="password_reset_confirm"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('apps.api.urls')),
    path('authentication/', include('dj_rest_auth.urls')),
    path('authentication/registration/',
         include('dj_rest_auth.registration.urls')),
    # Email management
    path('resend_verification_email/<int:email_id>/',
         profile_views.resend_verification_email),
    re_path(r'confirm_email/(?P<key>[-:\w]+)/$',
            profile_views.confirm_email, name="account_confirm_email"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
