# coding: utf-8
from __future__ import unicode_literals

from rest_framework import serializers
from datetime import datetime

from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', )