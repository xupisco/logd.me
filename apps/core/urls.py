# coding: utf-8

from __future__ import unicode_literals

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home',),
    url(r'^login$', views.login, name='login',),
    url(r'^people$', views.people, name='people',),
    url(r'^companies$', views.companies, name='companies',),
    url(r'^calendar$', views.calendar, name='calendar',),
]