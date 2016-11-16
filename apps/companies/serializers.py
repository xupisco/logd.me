# coding: utf-8
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Company
from ..people.models import Person


class BasicPeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name', 'email', )


class CompanySerializer(serializers.ModelSerializer):
    people =  BasicPeopleSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'domain', 'people', )
