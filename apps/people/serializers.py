# coding: utf-8
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Person


class PersonSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    role = serializers.StringRelatedField()

    class Meta:
        model = Person
        fields = ('company', 'role', 'name', 'email', 'mobile', 'landline', )
