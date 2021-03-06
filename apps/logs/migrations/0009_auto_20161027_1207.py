# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-27 14:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0008_auto_20161027_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='companies',
            field=models.ManyToManyField(blank=True, null=True, related_name='companies', to='companies.Company'),
        ),
        migrations.AlterField(
            model_name='log',
            name='people',
            field=models.ManyToManyField(blank=True, null=True, related_name='people', to='people.Person'),
        ),
    ]
