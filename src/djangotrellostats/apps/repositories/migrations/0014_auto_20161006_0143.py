# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-05 23:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0030_auto_20160925_1843'),
        ('repositories', '0013_auto_20160927_1935'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='pylintmessage',
            index_together=set([('board', 'repository', 'commit', 'commit_file', 'type'), ('board', 'commit', 'type'), ('board', 'type'), ('board', 'repository', 'type', 'commit', 'commit_file'), ('commit', 'type', 'commit_file'), ('commit', 'type'), ('commit', 'commit_file', 'type')]),
        ),
    ]
