from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from ..companies.models import Company


class Role(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(_('name'), max_length=255)
    slug = models.CharField(_('slug'), max_length=255, blank=False)

    def __unicode__(self):
        return self.name


class Person(models.Model):
    owner = models.ForeignKey(User)
    company = models.ForeignKey(Company, related_name='people', null=True, blank=True)
    role = models.ForeignKey(Role, null=True, blank=True)
    name = models.CharField(_('name'), max_length=255)
    email = models.CharField(_('email'), max_length=255, blank=True)

    mobile = models.CharField(_('mobile'), max_length=32, blank=True)
    landline = models.CharField(_('landline'), max_length=32, blank=True)

    created_on = models.DateTimeField(_('created on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'), auto_now=True)

    def __unicode__(self):
        if self.company:
            return "{0} - {1} @ {2}".format(self.name, self.role, self.company)
        else:
            return self.name

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('people')


class EmploymentLog(models.Model):
    person = models.ForeignKey(Person)
    last_company = models.ForeignKey(Company)

    created_on = models.DateTimeField(_('created on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'), auto_now=True)

    def __unicode__(self):
        return "{0} {1} {2}".format(self.person, _('was working at'), self.last_company)
