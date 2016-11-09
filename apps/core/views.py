# coding: utf-8

from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import translation

import json

from ..logs.models import LogKind
from ..people.models import Person


class StaticView(View):
    page_title = ""
    template_name = ""

    def get(self, request):
        return render(request, self.template_name, {'page_title': self.page_title})


def set_language(request, lang_code):

    if translation.check_for_language(lang_code):
        translation.activate(lang_code)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang_code

    return redirect('/')


def login(request):
    context = {
        'hello': 'world'
    }
    return render(request, 'login.html', context)


@login_required
def home(request):
    kinds = LogKind.objects.filter(owner=request.user).order_by('name')

    context = {
        'kinds': kinds
    }
    return render(request, 'timeline.html', context)


@login_required
def people(request):
    ppl = Person.objects \
        .filter(owner=request.user) \
        .order_by('name') \
        .values('name', 'company__name', 'role__name', 'email', 'mobile', 'created_on')
    ppl_json = json.dumps(list(ppl), cls=DjangoJSONEncoder)
    context = {
        'people': ppl_json
    }
    return render(request, 'people.html', context)


@login_required
def companies(request):
    context = {
        'dude': 'Alaor'
    }
    return render(request, 'companies.html', context)


@login_required
def calendar(request):
    context = {
        'dude': 'Alaor'
    }
    return render(request, 'calendar.html', context)
