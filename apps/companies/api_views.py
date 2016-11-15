# coding: utf-8

from rest_framework import viewsets

from .models import Company
from .serializers import CompanySerializer


class CompaniesViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer

    def get_queryset(self):
        companies = Company.objects.filter(owner=self.request.user).order_by('name')

        return companies
