# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-25 22:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0008_auto_20160923_2056'),
        ('boards', '0030_auto_20160925_1843'),
    ]

    operations = [
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('slug', models.SlugField(max_length=64, unique=True, verbose_name='Slug for this journal entry')),
                ('uuid', models.CharField(max_length=16, unique=True, verbose_name='Unique uuid for short urls')),
                ('content', models.TextField(help_text='Content of this journal entry', verbose_name='Content')),
                ('creation_datetime', models.DateTimeField(verbose_name='Creation datetime')),
                ('last_update_datetime', models.DateTimeField(verbose_name='Last update datetime')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journal_entries', to='members.Member', verbose_name='Member')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journal_entries', to='boards.Board', verbose_name='Board')),
            ],
        ),
    ]
