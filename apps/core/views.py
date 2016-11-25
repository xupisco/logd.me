# coding: utf-8

from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import translation
from django.utils.text import slugify
from django.conf import settings

import json
import re
from datetime import datetime

from ..logs.models import Log, LogKind
from ..people.models import Person, Role
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
    # if request.META['HTTP_USER_AGENT'].find('face') == -1:
    #     if not request.session.get(translation.LANGUAGE_SESSION_KEY):
    #         return redirect('/set_language/' + settings.LANGUAGE_CODE)

    return render(request, 'login.html')


def public(request, encoded):
    from hashids import Hashids
    hashids = Hashids(salt=settings.SECRET_KEY)
    decoded = hashids.decode(encoded)

    try:
        log = Log.objects.get(id=decoded[1], owner=decoded[0])
        if not log.public:
            return redirect('/')

        log.public_views = log.public_views + 1
        log.save()

        return render(request, 'public.html', {'public': True, 'log': log})
    except:
        return redirect('/')


@login_required
def home(request):
    from conf.utils import glyphicon_classes

    if not request.session.get(translation.LANGUAGE_SESSION_KEY):
        return redirect('/set_language/' + settings.LANGUAGE_CODE)

    user_log_count = Log.objects.filter(owner=request.user).count()
    if not user_log_count:
        create_default_log(request)

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
        'mentions': mentions,
        'q': request.GET.get('q', '')
    }
    return render(request, 'timeline.html', context)


@login_required
def people(request):
    companies = Company.objects.filter(owner=request.user).order_by('name')
    roles = Role.objects.filter(owner=request.user).order_by('name')
    context = {
        'companies': companies,
        'roles': roles
    }
    return render(request, 'people.html', context)


@login_required
def companies(request):
    companies = Company.objects.filter(owner=request.user).order_by('name')
    context = {
        'companies': companies
    }
    return render(request, 'companies.html', context)


@login_required
def calendar(request):
    context = {
        'dude': 'Alaor'
    }
    return render(request, 'calendar.html', context)


# Temp stuff
def newcompany(request):
    ncompany_name = request.POST.get('ncompany_name')
    ncompany_phone = request.POST.get('ncompany_phone')
    is_update = int(request.POST.get('is_update'))

    if not is_update:
        company = Company(
            owner=request.user,
            name=ncompany_name,
            phone=ncompany_phone)
    else:
        company = Company.objects.get(id=is_update)
        old_name = company.name
        company.name = ncompany_name
        company.phone = ncompany_phone

        if ncompany_name != old_name:
            logs = Log.objects.filter(companies=company)
            base_string = '<span class="hl_mention_{0}" data-id="{1}">{2}</span>'

            for log in logs:
                old_string = base_string.format('company', company.id, old_name)
                new_string = base_string.format('company', company.id, ncompany_name)

                log.body = log.body.replace(old_string, new_string)
                log.save()

    company.save()

    response_data = {}
    response_data['success'] = True

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def removecompany(request):
    company_id = request.POST.get('company_id')
    company = Company.objects.filter(owner=request.user).filter(id=company_id)

    response_data = {}
    if not company:
        response_data['success'] = False
    else:
        place = company[0]
        logs = Log.objects.filter(companies=place)
        base_string = '<span class="hl_mention_{0}" data-id="{1}">{2}</span>'

        for log in logs:
            old_string = base_string.format('company', place.id, place.name)
            new_string = place.name

            log.body = log.body.replace(old_string, new_string)
            log.save()

        company.delete()
        response_data['success'] = True

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def newperson(request):
    nppl_name = request.POST.get('nppl_name')
    nppl_company = request.POST.get('nppl_company')
    nppl_role = request.POST.get('nppl_role')
    nppl_email = request.POST.get('nppl_email')
    nppl_mobile = request.POST.get('nppl_mobile')
    nppl_company_new = request.POST.get('nppl_company_new')
    nppl_role_new = request.POST.get('nppl_role_new')
    is_update = int(request.POST.get('is_update'))

    nppl_company_text = nppl_company_new if len(nppl_company_new) > 1 else False
    nppl_role_text = nppl_role_new if len(nppl_role_new) > 1 else False

    if nppl_company_new:
        nppl_company, created = Company.objects.get_or_create(
            owner=request.user,
            name=nppl_company_text)
    else:
        if nppl_company == "0":
            nppl_company = None
        else:
            nppl_company = Company.objects.get(id=nppl_company)

    if nppl_role_new:
        nppl_role, created = Role.objects.get_or_create(
            owner=request.user,
            name=nppl_role_text)
    else:
        if nppl_role == "0":
            nppl_role = None
        else:
            nppl_role = Role.objects.get(id=nppl_role)

    if not is_update:
        ppl = Person(
            owner=request.user,
            name=nppl_name,
            email=nppl_email,
            mobile=nppl_mobile)
        ppl.save()
    else:
        ppl = Person.objects.get(id=is_update)
        old_name = ppl.name

        ppl.name = nppl_name
        ppl.email = nppl_email
        ppl.mobile = nppl_mobile

        if nppl_name != old_name:
            logs = Log.objects.filter(people=ppl)
            base_string = '<span class="hl_mention_{0}" data-id="{1}">{2}</span>'

            for log in logs:
                old_string = base_string.format('person', ppl.id, old_name)
                new_string = base_string.format('person', ppl.id, nppl_name)

                log.body = log.body.replace(old_string, new_string)
                log.save()

    ppl.company = nppl_company
    ppl.role = nppl_role
    ppl.save()

    response_data = {}
    response_data['success'] = True

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def newlog(request):
    # POG
    try:
        nkind_text = request.POST.get('nkind_text')
        nkind_icon = request.POST.get('nkind_icon')
        nlog_kind_id = request.POST.get('nlog_kind_id')
        nlog_start_date = request.POST.get('nlog_start_date')
        nlog_end_date = request.POST.get('nlog_end_date')
        nlog_highlight = request.POST.get('nlog_highlight')
        nlog_body = request.POST.get('nlog_body')
        is_update = int(request.POST.get('is_update'))

        mentions = parse_from_string(request, nlog_body)

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
                body=mentions['body']
            )
            nlog.save()
        else:
            nlog = Log.objects.get(id=is_update)
            nlog.kind = kind
            nlog.start_date = start_date
            nlog.end_date = end_date
            nlog.reminder = nlog_highlight
            nlog.body = mentions['body']

        nlog.companies = mentions['companies']
        nlog.people = mentions['people']
        nlog.save()

        response_data = {}
        response_data['success'] = True
    except:
        response_data = {}
        response_data['success'] = False

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


def removeperson(request):
    person_id = request.POST.get('person_id')
    person = Person.objects.filter(owner=request.user).filter(id=person_id)

    response_data = {}
    if not person:
        response_data['success'] = False
    else:
        dude = person[0]
        logs = Log.objects.filter(people=dude)
        base_string = '<span class="hl_mention_{0}" data-id="{1}">{2}</span>'

        for log in logs:
            old_string = base_string.format('person', dude.id, dude.name)
            new_string = dude.name

            log.body = log.body.replace(old_string, new_string)
            log.save()

        person.delete()
        response_data['success'] = True

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def changetheme(request):
    request.session['theme'] = request.POST.get('new_theme', '')

    response_data = {}
    response_data['success'] = True
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def changevisibility(request):
    status = int(request.POST.get('status', 0))
    log_id = request.POST.get('log_id')

    log = Log.objects.get(id=log_id)
    response_data = {}

    if not log:
        response_data['success'] = False
        response_data['encoded'] = ""
    else:
        response_data['success'] = True
        if status:
            from hashids import Hashids
            import random
            import hashlib

            hashids = Hashids(salt=settings.SECRET_KEY)
            fake_hash = int(filter(str.isdigit, hashlib.md5(str(123)).hexdigest())[:6])
            encoded = hashids.encode(log.owner.id, log.id, fake_hash)

            log.public = True
            response_data['encoded'] = '/pub/' + encoded
        else:
            log.public = False
            response_data['encoded'] = ""

        log.save()

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def parse_from_string(request, nlog_body):
    companies = []
    people = []

    parsed_companies = []
    parsed_people = []

    mentions_re = r"<span class=\"hl_mention_([^\"]+)\".*?\"([^\"]+)\".*?>(.*?)<\/span>"
    parsed_mentions = re.findall(mentions_re, nlog_body)

    base_string = '<span class="hl_mention_{0}" data-id="{1}">{2}</span>'

    for mention in parsed_mentions:
        if mention[0] == 'company':
            if int(mention[1]) == 0:
                c_exists = Company.objects.filter(owner=request.user,
                                                  name=mention[2])

                if not c_exists:
                    nlog_company = Company(owner=request.user,
                                           name=mention[2])
                    nlog_company.save()

                    old_string = base_string.format('company', '0', mention[2])
                    new_string = base_string.format('company', nlog_company.id, mention[2])

                    nlog_body = nlog_body.replace(old_string, new_string)
                    parsed_companies.append(nlog_company.id)
                else:
                    place = c_exists[0]
                    old_string = base_string.format('company', '0', mention[2])
                    new_string = base_string.format('company', place.id, mention[2])

                    nlog_body = nlog_body.replace(old_string, new_string)
                    parsed_companies.append(c_exists[0].id)
            else:
                parsed_companies.append(mention[1])

        if mention[0] == 'person':
            if int(mention[1]) == 0:
                p_exists = Person.objects.filter(owner=request.user, name=mention[2])

                if not p_exists:
                    nlog_person = Person(owner=request.user,
                                         name=mention[2])
                    nlog_person.save()

                    old_string = base_string.format('person', '0', mention[2])
                    new_string = base_string.format('person', nlog_person.id, mention[2])

                    nlog_body = nlog_body.replace(old_string, new_string)
                    parsed_people.append(nlog_person.id)
                else:
                    dude = p_exists[0]
                    old_string = base_string.format('person', '0', mention[2])
                    new_string = base_string.format('person', dude.id, mention[2])

                    nlog_body = nlog_body.replace(old_string, new_string)
                    parsed_people.append(p_exists[0].id)
            else:
                parsed_people.append(mention[1])

    if len(parsed_companies):
        companies = Company.objects.filter(owner=request.user) \
            .filter(id__in=parsed_companies)

    if len(parsed_people):
        people = Person.objects.filter(owner=request.user) \
            .filter(id__in=parsed_people)

    return {
        'body': nlog_body,
        'companies': companies,
        'people': people
    }


def create_default_log(request):
    from ..logs.default_log import body
    log_body = body(translation.get_language())

    mentions = parse_from_string(request, log_body)
    start_date = datetime.now()

    # Create default category
    kind, created = LogKind.objects.get_or_create(
        owner=request.user,
        name='Inbox',
        slug='inbox',
        glyphicon_name='inbox'
    )

    nlog = Log(
        owner=request.user,
        kind=kind,
        start_date=start_date,
        end_date=None,
        reminder=False,
        body=mentions['body']
    )
    nlog.save()

    # Update default peoplo and company
    company = Company.objects.get(name="ACME Corporation", owner=request.user)
    gill_bates = Person.objects.get(name="Gill Bates", owner=request.user)
    john_doe = Person.objects.get(name="John Doe", owner=request.user)
    default_role, created = Role.objects.get_or_create(name="CEO",
                                                       slug='ceo',
                                                       owner=request.user)

    gill_bates.email = "gillbates@acme.org"
    gill_bates.mobile = "555-1234"
    gill_bates.role = default_role
    gill_bates.company = company
    gill_bates.save()

    john_doe.email = "john@doe.net"
    john_doe.save()

    nlog.companies = mentions['companies']
    nlog.people = mentions['people']
    nlog.save()
