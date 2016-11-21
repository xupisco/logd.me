from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify


class Company(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(_('name'), max_length=128)
    slug = models.CharField(_('slug'), max_length=255, blank=False)
    phone = models.CharField(_('phone'), max_length=32, blank=True)
    domain = models.URLField(_('domain'), blank=True)

    created_on = models.DateTimeField(_('created on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'), auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('company')
        verbose_name_plural = _('companies')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super(Company, self).save(*args, **kwargs)
