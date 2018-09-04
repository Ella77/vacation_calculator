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
    2. Add a URL to urlpatterns:  path('datepick/', include('datepick.urls'))
"""
from django.contrib import admin
from django.urls import path

from datepick.views import *

from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from .feedback import MailToAdmin

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^post/replace/new/$', replace_new, name='replace_new'),
    url(r'^post/new/year/full$', post_new_year_full,name= 'post_new_year_full'),
    url(r'^post/full$', post_full, name='post_full'),
    url(r'^post/new/half$', post_new_half, name='post_new_half'),
    url(r'^post/new/full$',post_new_full,name='post_new_full'),
    url(r'^post/new/special$',post_special,name = 'post_special'),
    url(r'^post/new/special_new$',post_special_new,name='post_special_new'),
    url(r'^post/new/$',post_new, name= 'post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', edit, name='post_edit_entry'),
    url(r'^post/(?P<pk>\d+)/approve/$', approve, name='approve'),
    url(r'^main/$', main, name='main'),
    url(r'^list_admin/', list_admin,name='list_admin'),
    url(r'^list/$', list,name='list'),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(),name='login'),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(),name='logout'),
    url(r'^post/(?P<pk>\d+)/editsample/$', post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/remove/$',post_remove,name= 'post_remove'),
    url(r'^help/$', help, name='help'),
    url(r'^setting/$', setting,name='setting'),
    url(r'^list/admin/$',list,name='list'),
    url(r'^django_popup_view_field/',include('django_popup_view_field.urls')
        ),
    url(r'^list_user/(?P<pk>\d+)/$',list_user,name='list_user'),
    url(r'^ContactToAdmin$', MailToAdmin),
    url(r'^$',confirm,name='confirm'),
    url(r'^vacation/<int:pk>', VacationListbyAuthor.as_view(), name='vacation-by-author'),
    url(r'^vacations/', VacationerListView.as_view(), name= 'bloggers'),

]
