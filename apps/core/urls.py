# coding: utf-8

from __future__ import unicode_literals

from django.conf.urls import include, url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home',),
    url(r'^pub/(?P<encoded>[\w-]+)/?$', views.public, name='public',),
    url(r'^login$', views.login, name='login',),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^set_language/(?P<lang_code>[\w-]+)$', views.set_language, name='set_language'),
    url(r'^people$', views.people, name='people',),
    url(r'^companies$', views.companies, name='companies',),
    url(r'^calendar$', views.calendar, name='calendar',),

    # Temp stuff
    url(r'^ajax/new_log$', views.newlog, name='newlog',),
    url(r'^ajax/remove_log$', views.removelog, name='removelog',),

    url(r'^ajax/new_person$', views.newperson, name='newperson',),
    url(r'^ajax/remove_person$', views.removeperson, name='removeperson',),

    url(r'^ajax/new_company$', views.newcompany, name='newcompany',),
    url(r'^ajax/remove_company$', views.removecompany, name='removecompany',),
]
