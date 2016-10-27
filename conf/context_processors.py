# coding: utf-8
from __future__ import unicode_literals

from django.conf import settings


def settings_context(request):

    return {
        'DEBUG': settings.DEBUG,
        'SITE_NAME': settings.SITE_NAME,
        'OG_DESCRIPTION': settings.OG_DESCRIPTION,
        'GTM_ID': settings.GTM_ID,
    }
