# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 18:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0011_logkind_glyphicon_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logkind',
            name='glyphicon_name',
            field=models.CharField(blank=True, default='', max_length=32, verbose_name='icon'),
        ),
    ]
