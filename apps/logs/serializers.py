# coding: utf-8
from __future__ import unicode_literals

from django.utils.html import linebreaks
from django.utils.safestring import mark_safe
from django.conf import settings

from rest_framework import serializers
from datetime import datetime
from hashids import Hashids
import random
import hashlib

from .models import Log, LogKind
from ..companies.serializers import CompanySerializer
from ..people.serializers import PersonSerializer


class KindSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogKind
        fields = ('id', 'name', 'slug', 'glyphicon_name', )


class LogSerializer(serializers.ModelSerializer):
    kind = KindSerializer()
    hashtags = serializers.JSONField()
    companies = CompanySerializer(read_only=True, many=True)
    people = PersonSerializer(read_only=True, many=True)
    public_url = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()

    class Meta:
        model = Log
        fields = (
            'id', 'kind', 'body', 'hashtags', 'companies', 'people',
            'start_date', 'end_date', 'reminder', 'created_on',
            'updated_on', 'meta', 'public_url', 'public', 'public_views'
        )

    def get_public_url(self, obj):
        if obj.public:
            hashids = Hashids(salt=settings.SECRET_KEY)
            fake_hash = int(filter(str.isdigit, hashlib.md5(str(123)).hexdigest())[:6])
            return hashids.encode(obj.owner.id, obj.id, fake_hash)
        else:
            return False

    # todo: fix this...
    def get_meta(self, obj):
        people = ', '.join(
            str(val) for val in obj.people.values_list('name', 'email', )
        )
        companies = ', '.join(
            str(val) for val in obj.companies.values_list('name', )
        )

        highligh = "!!!" if obj.reminder else ""

        res = list(obj.people.values_list('name', 'email')) + \
            list(obj.companies.values_list('name'))

        return ', '.join(tuple([x[0] for x in res])) + ', ' + highligh
