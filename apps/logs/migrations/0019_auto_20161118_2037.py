# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-18 22:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0018_log_public_view'),
    ]

    operations = [
        migrations.RenameField(
            model_name='log',
            old_name='public_view',
            new_name='public_views',
        ),
    ]
