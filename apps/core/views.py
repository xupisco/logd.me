# coding: utf-8

from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.views.generic import View

from ..people.models import Person


class StaticView(View):
    page_title = ""
    template_name = ""

    def get(self, request):
        return render(request, self.template_name, { 'page_title': self.page_title })


def home(request):
    context = {
        'dude': 'Alaor'
    }
    return render(request, 'timeline.html', context)


def people(request):
    context = {
        'people': Person.objects.order_by('name')
    }
    return render(request, 'people.html', context)


def companies(request):
    context = {
        'dude': 'Alaor'
    }
    return render(request, 'companies.html', context)


def calendar(request):
    context = {
        'dude': 'Alaor'
    }
    return render(request, 'calendar.html', context)