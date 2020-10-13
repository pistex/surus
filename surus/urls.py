"""surus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.shortcuts import redirect


def password_reset_frontend_redirect(request, uidb64, token):
    response = redirect('http://localhost:8080/password_reset/'+uidb64+'/'+token)
    return response

urlpatterns = [
    re_path(r"^authentication/password/reset/key/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$",
            password_reset_frontend_redirect,
            name="password_reset_confirm"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('apps.api.urls')),
    path('debugger/', include('apps.debugger.urls')),
    path('authentication/', include('dj_rest_auth.urls')),
    path('authentication/registration/', include('dj_rest_auth.registration.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
