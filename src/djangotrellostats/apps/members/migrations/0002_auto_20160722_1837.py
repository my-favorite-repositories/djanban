# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-22 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_developer',
            field=models.BooleanField(default=False, help_text='Informs if this member is a developer and hence will receive reportsand other information', verbose_name='Is this member a developer?'),
        ),
        migrations.AddField(
            model_name='member',
            name='on_holidays',
            field=models.BooleanField(default=False, help_text='If the developer is on holidays will stop receiving reportsand other emails', verbose_name='Is this developer on holidays?'),
        ),
    ]
