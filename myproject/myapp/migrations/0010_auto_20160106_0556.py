# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-06 05:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20160106_0535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='shared',
            field=models.BooleanField(default=True),
        ),
    ]
