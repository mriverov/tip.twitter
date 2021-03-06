# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-25 23:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mole', '0005_centralityurl'),
    ]

    operations = [
        migrations.CreateModel(
            name='CentralityHashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(blank=True, null=True)),
                ('centrality', models.FloatField(blank=True, default=0.0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(blank=True, null=True)),
                ('hashtag', models.CharField(blank=True, max_length=5000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HashtagGraph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_oid_i', models.BigIntegerField(blank=True, null=True)),
                ('user_oid_j', models.BigIntegerField(blank=True, null=True)),
                ('ratio', models.FloatField(blank=True, default=0.0, null=True)),
            ],
        ),
    ]
