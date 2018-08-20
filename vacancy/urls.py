"""vacancy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from datepick.views import post_new,main,list,post_edit,post_remove, help,setting
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',main,name='main'),
    url(r'^post/new/$', post_new, name='post_new'),
    url(r'^main/$', main, name='main'),
    url(r'^list/$', list,name='list'),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(),name='login'),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(),name='logout'),
    url(r'^post/(?P<pk>\d+)/edit/$', post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/remove/$',post_remove,name= 'post_remove'),
    url(r'^help/$', help, name='help'),
    url(r'^setting/$', setting,name='setting'),

]
