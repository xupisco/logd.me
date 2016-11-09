# coding: utf-8

from rest_framework import viewsets

from .models import Log
from .serializers import LogSerializer


class LogsViewSet(viewsets.ModelViewSet):
    serializer_class = LogSerializer

    def get_queryset(self):
        logs = Log.objects.filter(owner=self.request.user).order_by('-start_date')

        return logs
