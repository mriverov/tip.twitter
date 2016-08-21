# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-20 23:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mole', '0008_urls_project_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='centralityhashtag',
            name='project_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='centralityurl',
            name='project_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hashtaggraph',
            name='project_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='urls',
            name='tweet_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='urlsgraph',
            name='project_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
