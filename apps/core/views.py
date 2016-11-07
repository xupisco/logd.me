# coding: utf-8

from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.core.serializers.json import DjangoJSONEncoder

import json

from ..logs.models import Log, LogKind
from ..people.models import Person


class StaticView(View):
    page_title = ""
    template_name = ""

    def get(self, request):
        return render(request, self.template_name, { 'page_title': self.page_title })


def home(request):
    kinds = LogKind.objects.order_by('name')

    context = {
        'kinds': kinds
    }
    return render(request, 'timeline.html', context)


def people(request):
    ppl = Person.objects.order_by('name').values('name', 'company__name', 'role__name', 'email', 'mobile', 'created_on')
    ppl_json = json.dumps(list(ppl), cls=DjangoJSONEncoder)
    context = {
        'people': ppl_json
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