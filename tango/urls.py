"""tango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.staticfiles.views import serve
#settings gives access to variables inside settings.py
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.simple.views import RegistrationView
class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return '/rango/'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('rango.urls')),
    url(r'^rango/', include('rango.urls')),
    #simple gives these machinery
    #registration -> /accounts/register/
    #registration complete -> /accounts/register/complete
    #login -> /accounts/login/
    #logout -> /accounts/logout/
    #password change -> /password/change/
    #password reset -> /password/reset/
    #change simple to default to get activation (emails, etc... 2 step registration)
    #need templates for all of these views: https://github.com/macdhuibh/django-registration-templates
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    #url(r'^password/', include('registration.backends.simple.urls')),
]
#] + static(settings.MEDIA_URL,
#           document_root = settings.MEDIA_ROOT)

#skip for now gg... go to part 5 of tutorial later

#if settings.DEBUG:
#    urlpatterns += patterns[
#        'django.views.static',
#        (r'^media/(?P<path>.*)$',
#        serve,
#        {'document_root': settings.MEDIA_ROOT}) ]

#if settings.DEBUG:
#    urlpatterns += [
#        url(r'^media/(?P<path>.*)$', views.serve),