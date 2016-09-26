# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-26 16:51
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0002_auto_20160926_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalentry',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(help_text='Content of this journal entry', verbose_name='Content'),
        ),
    ]
