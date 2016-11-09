from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from markdown import markdown
import re
import json

from ..companies.models import Company
from ..people.models import Person


class LogKind(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(_('name'), max_length=255)
    slug = models.CharField(_('slug'), max_length=255, blank=False)
    glyphicon_name = models.CharField(_('icon'), max_length=32, blank=True, default='')

    def __unicode__(self):
        return self.name


class Log(models.Model):
    owner = models.ForeignKey(User)
    kind = models.ForeignKey(LogKind)
    body = models.TextField()
    start_date = models.DateTimeField(_('date start'), blank=False)
    end_date = models.DateTimeField(_('date end'), blank=True, null=True)

    reminder = models.BooleanField(_('reminder'), default=False)

    companies = models.ManyToManyField(Company, related_name='companies', blank=True)
    people = models.ManyToManyField(Person, related_name='people', blank=True)

    created_on = models.DateTimeField(_('created on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'), auto_now=True)

    def __unicode__(self):
        return self.kind.name

    @property
    def body_md(self):
        return markdown(re.sub(r"#(\w+)", '', self.body))

    @property
    def hashtags(self):
        return re.findall(r"#(\w+)", self.body)


    @body_md.setter
    def body_md(self, value):
        self.body = value
