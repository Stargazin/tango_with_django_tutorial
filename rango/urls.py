#read this eventually:
#https://docs.djangoproject.com/en/1.7/topics/http/urls/#how-django-processes-a-request
#key point being django processes urlpatterns in order and stops at whichever one matches first
#not sure if this means if you are looking for 'a' and you have both 'aa' and 'a', it will match with 'aa'
#or it has to be exact match
from django.conf.urls import url
from . import views

#don't forget commas for tuples... pls lol
urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^rango/$', views.index, name='index'),
    url(r'^rango/about/$', views.about, name='about'),
    #[\w\-]+... \w means any sequence of a-z, A-Z, or 0-9 and - is the dash for our slug
    #so you get aaa-bbb-ccc of any amount (b/c of +)
    url(r'^rango/add_category/$', views.add_category, name='add_category'),
    url(r'^rango/category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^rango/category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^rango/register/$', views.register, name='register'),
]