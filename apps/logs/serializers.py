# coding: utf-8
from __future__ import unicode_literals

from django.utils.html import linebreaks
from django.utils.safestring import mark_safe

from rest_framework import serializers
from datetime import datetime
from markdown import markdown

from .models import Log, LogKind
from ..companies.serializers import CompanySerializer
from ..people.serializers import PersonSerializer


class KindSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogKind
        fields = ('name', 'slug', 'glyphicon_name', )


class LogSerializer(serializers.ModelSerializer):
    kind = KindSerializer()
    body = serializers.SerializerMethodField()
    companies = CompanySerializer(read_only=True, many=True)
    people = PersonSerializer(read_only=True, many=True)
    meta = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()

    class Meta:
        model = Log
        fields = ('kind', 'body', 'companies', 'people', 'start_date', 'end_date', 'reminder', 'created_on', 'updated_on', 'meta')

    def get_body(self, obj):
        return markdown(obj.body)

    def get_start_date(self, obj):
        return obj.start_date.strftime("%d/%m/%Y %H:%M")

    def get_end_date(self, obj):
        return obj.end_date.strftime("%d/%m/%Y %H:%M") if obj.end_date else False

    #todo: fix this...
    def get_meta(self, obj):
        people = ', '.join(str(val) for val in obj.people.values_list('name', 'email', ))
        companies = ', '.join(str(val) for val in obj.companies.values_list('name', ))
        return '{0}, {1}'.format(people, companies)