# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-09 18:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0011_trellomemberprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='api_key',
        ),
        migrations.RemoveField(
            model_name='member',
            name='api_secret',
        ),
        migrations.RemoveField(
            model_name='member',
            name='initials',
        ),
        migrations.RemoveField(
            model_name='member',
            name='token',
        ),
        migrations.RemoveField(
            model_name='member',
            name='token_secret',
        ),
        migrations.RemoveField(
            model_name='member',
            name='trello_username',
        ),
        migrations.RemoveField(
            model_name='member',
            name='uuid',
        ),
        migrations.AlterField(
            model_name='trellomemberprofile',
            name='member',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trello_member_profile', to='members.Member', verbose_name='Associated member'),
        ),
    ]
