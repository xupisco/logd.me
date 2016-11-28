# coding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.utils import translation


def settings_context(request):

    user_theme = ''
    try:
        user_theme = request.session['theme']
    except:
        pass

    user_lang = ''
    try:
        user_lang = request.session[translation.LANGUAGE_SESSION_KEY]
    except:
        user_lang = settings.LANGUAGE_CODE

    return {
        'DEBUG': settings.DEBUG,
        'SITE_NAME': settings.SITE_NAME,
        'OG_DESCRIPTION': settings.OG_DESCRIPTION,
        'GTM_ID': settings.GTM_ID,
        'LANG': user_lang,
        'THEME': user_theme
    }
