# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-23 23:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0036_board_background_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='title_color',
            field=models.CharField(default='FFFFFF', help_text='Title color for this board in hexadecimal', max_length=32, verbose_name='Title color for this board'),
        ),
    ]