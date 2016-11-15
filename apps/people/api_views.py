# coding: utf-8

from rest_framework import viewsets

from .models import Person
from .serializers import PersonSerializer


class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer

    def get_queryset(self):
        people = Person.objects.filter(owner=self.request.user).order_by('name')

        return people
