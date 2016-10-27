from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _

from ..companies.models import Company
from ..people.models import Person


class LogKind(models.Model):
    name = models.CharField(_('name'), max_length=255)
    slug = models.CharField(_('slug'), max_length=255, blank=False)

    def __unicode__(self):
        return self.name


class Log(models.Model):
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

    
    