# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-19 04:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('troll', '0002_auto_20160319_0310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='key',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
