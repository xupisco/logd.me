# coding: utf-8

from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import translation

import json
from datetime import datetime

from ..logs.models import Log, LogKind
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
    from conf.utils import glyphicon_classes
    kinds = LogKind.objects.filter(owner=request.user).order_by('name')

    context = {
        'glyphicon_classes': glyphicon_classes,
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


# Temp stuff
def newlog(request):
    nkind_text = request.POST.get('nkind_text')
    nkind_icon = request.POST.get('nkind_icon')
    nlog_kind_id = request.POST.get('nlog_kind_id')
    nlog_start_date = request.POST.get('nlog_start_date')
    nlog_end_date = request.POST.get('nlog_end_date')
    nlog_highlight = request.POST.get('nlog_highlight')
    nlog_body = request.POST.get('nlog_body')

    nkind_text = nkind_text if len(nkind_text) > 1 else False
    nlog_end_date = nlog_end_date if len(nlog_end_date) > 1 else False
    nlog_highlight = True if nlog_highlight == 'true' else False

    kind = LogKind.objects.get(id=nlog_kind_id)

    start_date = datetime.strptime(nlog_start_date, "%d/%m/%Y %H:%M")
    end_date = datetime.strptime(nlog_end_date, "%d/%m/%Y %H:%M") if nlog_end_date else None

    nlog = Log (
            owner = request.user,
            kind = kind,
            start_date = start_date,
            end_date = end_date,
            reminder = nlog_highlight,
            body = nlog_body
        )

    nlog.save()

    response_data = {}
    response_data['success'] = True

    return HttpResponse(json.dumps(response_data), content_type="application/json")
