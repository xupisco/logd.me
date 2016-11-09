# coding: utf-8
from __future__ import unicode_literals

from django.utils.html import linebreaks
from django.utils.safestring import mark_safe

from rest_framework import serializers
from datetime import datetime

from .models import Log, LogKind
from ..companies.serializers import CompanySerializer
from ..people.serializers import PersonSerializer


class KindSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogKind
        fields = ('id', 'name', 'slug', 'glyphicon_name', )


class LogSerializer(serializers.ModelSerializer):
    kind = KindSerializer()
    body_md = serializers.CharField()
    companies = CompanySerializer(read_only=True, many=True)
    people = PersonSerializer(read_only=True, many=True)
    meta = serializers.SerializerMethodField()

    class Meta:
        model = Log
        fields = (
            'id', 'kind', 'body_md', 'companies', 'people',
            'start_date', 'end_date', 'reminder', 'created_on',
            'updated_on', 'meta'
        )

    # todo: fix this...
    def get_meta(self, obj):
        people = ', '.join(str(val) for val in obj.people.values_list('name', 'email', ))
        companies = ', '.join(str(val) for val in obj.companies.values_list('name', ))
        return '{0}, {1}'.format(people, companies)
