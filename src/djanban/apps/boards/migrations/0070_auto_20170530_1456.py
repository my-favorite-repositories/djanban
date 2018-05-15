# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-30 12:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0069_auto_20170530_1425'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='card',
            index_together=set([('board', 'is_closed', 'list', 'position'), ('board', 'creation_datetime', 'list'), ('board', 'list', 'position'), ('is_closed', 'board', 'creation_datetime', 'list', 'number_of_forward_movements', 'number_of_backward_movements'), ('board', 'creation_datetime'), ('board', 'due_datetime'), ('board', 'is_closed', 'creation_datetime', 'list', 'number_of_forward_movements', 'number_of_backward_movements'), ('board', 'list', 'number_of_forward_movements', 'number_of_backward_movements', 'creation_datetime')]),
        ),
    ]