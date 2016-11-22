"""
WSGI config for tenda project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import settings

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)

try:
    from newrelic import agent
    newrelic.agent.initialize(os.path.join(settings.BASE_DIR, 'conf') + '/newrelic.ini')

    application = newrelic.agent.wsgi_application()(application)
except:
    pass
