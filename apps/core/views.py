# coding: utf-8

from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import translation
from django.utils.text import slugify

import json
import re
from datetime import datetime

from ..logs.models import Log, LogKind
from ..people.models import Person
from ..companies.models import Company


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
    return render(request, 'login.html')


@login_required
def home(request):
    from conf.utils import glyphicon_classes
    kinds = LogKind.objects.filter(owner=request.user).order_by('name')

    people_mentions = Person.objects.filter(owner=request.user) \
        .order_by('name') \
        .values('id', 'name', 'email')
    company_mentions = Company.objects.filter(owner=request.user) \
        .order_by('name') \
        .values('id', 'name')

    for p in people_mentions:
        p.update({'type': 'person'})

    for c in company_mentions:
        c.update({'email': '', 'type': 'company'})

    from itertools import chain
    combined = list(chain(people_mentions, company_mentions))

    mentions = json.dumps(list(combined), cls=DjangoJSONEncoder)

    context = {
        'glyphicon_classes': glyphicon_classes,
        'kinds': kinds,
        'mentions': mentions
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
    is_update = int(request.POST.get('is_update'))

    mentions_re = r"<span class=\"hl_mention_([^\"]+)\".*?\"([^\"]+)\".*?<\/span>"
    parsed_mentions = re.findall(mentions_re, nlog_body)

    nlog_companies = []
    nlog_people = []

    parsed_companies = []
    parsed_people = []

    for mention in parsed_mentions:
        if mention[0] == 'company':
            parsed_companies.append(mention[1])

        if mention[0] == 'person':
            parsed_people.append(mention[1])

    if len(parsed_companies):
        nlog_companies = Company.objects.filter(owner=request.user) \
            .filter(id__in=parsed_companies)

    if len(parsed_people):
        nlog_people = Person.objects.filter(owner=request.user) \
            .filter(id__in=parsed_people)

    nkind_text = nkind_text if len(nkind_text) > 1 else False
    nlog_end_date = nlog_end_date if len(nlog_end_date) > 1 else False
    nlog_highlight = True if nlog_highlight == 'true' else False

    if nkind_text:
        kind, created = LogKind.objects.get_or_create(
            owner=request.user,
            name=nkind_text,
            slug=slugify(nkind_text),
            glyphicon_name=nkind_icon
        )
    else:
        kind = LogKind.objects.get(id=nlog_kind_id)

    start_date = datetime.strptime(nlog_start_date, "%d/%m/%Y %H:%M")
    end_date = datetime.strptime(nlog_end_date, "%d/%m/%Y %H:%M") if nlog_end_date else None

    if not is_update:
        nlog = Log(
            owner=request.user,
            kind=kind,
            start_date=start_date,
            end_date=end_date,
            reminder=nlog_highlight,
            body=nlog_body,
            companies=nlog_companies,
            people=nlog_people
        )
    else:
        nlog = Log.objects.get(id=is_update)
        nlog.kind = kind
        nlog.start_date = start_date
        nlog.end_date = end_date
        nlog.reminder = nlog_highlight
        nlog.body = nlog_body
        nlog.companies = nlog_companies
        nlog.people = nlog_people

    nlog.save()

    response_data = {}
    response_data['success'] = True

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def removelog(request):
    log_id = request.POST.get('log_id')
    log = Log.objects.filter(owner=request.user).filter(id=log_id)

    response_data = {}
    if not log:
        response_data['success'] = False
    else:
        log.delete()
        response_data['success'] = True

    return HttpResponse(json.dumps(response_data), content_type="application/json")
