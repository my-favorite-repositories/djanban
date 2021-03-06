# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-15 15:31
from __future__ import unicode_literals

from django.db import migrations


def adjust_spent_time(member, spent_time, date):
    spent_time_factors = member.spent_time_factors.all()
    for spent_time_factor in spent_time_factors:
        if (spent_time_factor.start_date is None and spent_time_factor.end_date is None) or \
                (spent_time_factor.start_date <= date and spent_time_factor.end_date is None) or \
                (spent_time_factor.start_date <= date <= spent_time_factor.end_date):
            adjusted_value = spent_time * spent_time_factor.factor
            return adjusted_value
    return spent_time


def update_adjusted_spent_time(apps, schema):
    DailySpentTime = apps.get_model("dev_times", "DailySpentTime")
    for daily_spent_time in DailySpentTime.objects.all():
        if daily_spent_time.spent_time is None:
            daily_spent_time.adjusted_spent_time = None
        else:
            daily_spent_time.adjusted_spent_time = adjust_spent_time(
                daily_spent_time.member, daily_spent_time.spent_time, daily_spent_time.date
            )
        DailySpentTime.objects.filter(id=daily_spent_time.id).update(adjusted_spent_time=daily_spent_time.adjusted_spent_time)


class Migration(migrations.Migration):

    dependencies = [
        ('dev_times', '0008_dailyspenttime_adjusted_spent_time'),
    ]

    operations = [
        migrations.RunPython(update_adjusted_spent_time)
    ]
