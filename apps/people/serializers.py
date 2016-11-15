# coding: utf-8
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Person, Role
from ..companies.serializers import CompanySerializer


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', )


class PersonSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True, many=False)
    role = RoleSerializer(read_only=True, many=False)

    class Meta:
        model = Person
        fields = ('id', 'company', 'role', 'name', 'email', 'mobile', 'landline', )
