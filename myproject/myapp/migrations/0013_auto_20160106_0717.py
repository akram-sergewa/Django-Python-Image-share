# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-06 07:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_auto_20160106_0603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
