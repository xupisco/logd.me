# coding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.views import defaults as default_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('apps.core.urls', namespace='core')),

    url(r'^api/v1/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('apps.api.urls', namespace='api')),
    url(r'^api/?$', RedirectView.as_view(pattern_name='api:v1:api-root')),

    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^400/$',
            default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$',
            default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$',
            default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$',
            default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
