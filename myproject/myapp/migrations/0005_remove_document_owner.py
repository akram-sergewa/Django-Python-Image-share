# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-04 21:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20160104_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='owner',
        ),
    ]