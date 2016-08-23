# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-23 16:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0021_auto_20160823_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='enable_public_access',
            field=models.BooleanField(default=False, help_text='Only when enabled the users will be able to access', verbose_name='Enable public access to this board'),
        ),
        migrations.AlterField(
            model_name='board',
            name='public_access_code',
            field=models.CharField(help_text='With this code it is possible to access to a view with stats of this board', max_length=32, unique=True, verbose_name='External code of the board'),
        ),
    ]
