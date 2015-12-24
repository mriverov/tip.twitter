# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-13 18:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mole', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='trend',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mole.Trend'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.BigIntegerField(blank=True, db_index=True, null=True),
        ),
    ]