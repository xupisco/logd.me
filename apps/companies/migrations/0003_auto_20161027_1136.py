# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-27 13:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_auto_20161027_1111'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'company', 'verbose_name_plural': 'companies'},
        ),
    ]