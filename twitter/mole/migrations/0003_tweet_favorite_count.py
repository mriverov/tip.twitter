# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-13 22:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mole', '0002_auto_20151213_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='favorite_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
