# coding: utf-8

from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.views.generic import View


class StaticView(View):
    page_title = ""
    template_name = ""

    def get(self, request):
        return render(request, self.template_name, { 'page_title': self.page_title })


def home(request):
    context = {
        'dude': 'Alaor'
    }
    return render(request, 'index.html', context)    
