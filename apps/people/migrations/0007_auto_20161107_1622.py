# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 18:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0006_auto_20161107_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='companies.Company'),
        ),
        migrations.AlterField(
            model_name='person',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='people.Role'),
        ),
    ]