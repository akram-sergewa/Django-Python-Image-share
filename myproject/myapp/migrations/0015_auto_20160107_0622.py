# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-07 06:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_document_fx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='owner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.Drinker'),
        ),
    ]
