from django.conf.urls import url, include

from . import v1_urls


urlpatterns = [
    url(r'^v1/', include(v1_urls.urlpatterns, namespace='v1')),
]
