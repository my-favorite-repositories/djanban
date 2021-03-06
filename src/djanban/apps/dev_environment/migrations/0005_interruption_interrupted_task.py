# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-12 13:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dev_environment', '0004_interruption_spent_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='interruption',
            name='interrupted_task',
            field=models.TextField(blank=True, default='', help_text='Describe what were you doing when interrupted. This text has the aim of helping you return to your task once the interruption has ended.', verbose_name='What were you doing?'),
        ),
    ]
