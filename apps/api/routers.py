from rest_framework import routers
from rest_framework.reverse import reverse
from rest_framework import views
from rest_framework.permissions import AllowAny


class HybridRouter(routers.DefaultRouter):
    root_docs = "Root API endpoints."

    def __init__(self, *args, **kwargs):
        super(HybridRouter, self).__init__(*args, **kwargs)
        self.view_urls = []

    def add_url(self, view):
        self.view_urls.append(view)

    def get_urls(self):
        return super(HybridRouter, self).get_urls() + self.view_urls

    def get_api_root_view(self, api_urls=None):
        original_view = super(HybridRouter, self).get_api_root_view(api_urls=api_urls)
        original_view.cls.permission_classes = [AllowAny, ]

        class APIRoot(views.APIView):
            _ignore_model_permissions = True
            permission_classes = [AllowAny, ]

            def get(api_self, request, *args, **kwargs):
                resp = original_view(request, *args, **kwargs)
                namespace = request.resolver_match.namespace
                for view_url in self.view_urls:
                    name = view_url.name
                    url_name = name
                    if namespace:
                        url_name = namespace + ':' + url_name
                    resp.data[name] = reverse(
                        url_name,
                        args=args,
                        kwargs=kwargs,
                        request=request,
                        format=kwargs.get('format', None))
                return resp

        # APIRoot.__doc__ = self.root_docs

        return APIRoot.as_view()