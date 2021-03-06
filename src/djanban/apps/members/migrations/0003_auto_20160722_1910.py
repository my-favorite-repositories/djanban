# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-22 17:10
from __future__ import unicode_literals

from django.contrib.auth.models import Group
from django.db import migrations
from django.conf import settings


def create_administrator_group(apps, schema_editor):
    if not Group.objects.filter(name=settings.ADMINISTRATOR_GROUP).exists():
        administrators = Group(name=settings.ADMINISTRATOR_GROUP)
        administrators.save()


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20160722_1837'),
    ]

    operations = [
        migrations.RunPython(create_administrator_group),
    ]
