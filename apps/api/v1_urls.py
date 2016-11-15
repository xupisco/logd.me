from django.conf.urls import url

from rest_framework.authtoken import views as rest_views

from .routers import HybridRouter

from ..companies import api_views as companies_views
from ..logs import api_views as logs_views
from ..people import api_views as people_views


r = HybridRouter()
r.root_docs = """
Root API endpoints.
"""

r.register(r'logs', logs_views.LogsViewSet, base_name='logs')
r.register(r'companies', companies_views.CompaniesViewSet, base_name='companies')
r.register(r'people', people_views.PeopleViewSet, base_name='people')

r.view_urls = [
    url(r'^token-auth/?$', rest_views.obtain_auth_token, name='token-auth'),
]

urlpatterns = r.urls
