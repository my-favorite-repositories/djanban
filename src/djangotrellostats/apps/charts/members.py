# -*- coding: utf-8 -*-
import copy
import datetime
import pygal
from django.contrib.auth.decorators import login_required
from isoweek import Week

from django.db.models import Sum
from django.utils import timezone

from djangotrellostats.apps.base.auth import get_user_boards
from djangotrellostats.apps.boards.models import Board
from djangotrellostats.apps.dev_times.models import DailySpentTime
from djangotrellostats.apps.members.models import Member
from djangotrellostats.apps.reports.models import MemberReport


# Show a chart with the task movements (backward or forward) by member
from djangotrellostats.utils.week import number_of_weeks_of_year


def task_movements_by_member(movement_type="forward", board=None):
    if movement_type != "forward" and movement_type != "backward":
        raise ValueError("{0} is not recognized as a valid movement type".format(movement_type))

    chart_title = u"Task {0} movements as of {1}".format(movement_type, timezone.now())
    if board:
        chart_title += u" for board {0}".format(board.name)

    member_chart = pygal.HorizontalBar(title=chart_title, legend_at_bottom=True, print_values=True, print_zeroes=False,
                                       human_readable=True)

    report_filter = {}
    if board:
        report_filter["board_id"] = board.id

    members = Member.objects.all()

    for member in members:
        member_name = member.trello_username

        member_report_filter = copy.deepcopy(report_filter)
        member_report_filter["member"] = member

        try:
            # Depending on if the member report is filtered by board or not we only have to get the forward and
            # backward movements of a report or sum all the members report of this user
            if board:
                member_report = MemberReport.objects.get(**member_report_filter)
                forward_movements = member_report.forward_movements
                backward_movements = member_report.backward_movements

            else:
                member_reports = MemberReport.objects.filter(**member_report_filter)
                forward_movements = member_reports \
                    .aggregate(forward_movements_sum=Sum("forward_movements"))["forward_movements_sum"]
                backward_movements = member_reports \
                    .aggregate(backward_movements_sum=Sum("backward_movements"))["backward_movements_sum"]

            if movement_type == "forward":
                member_chart.add(u"{0}'s tasks forward movements".format(member_name), forward_movements)

            elif movement_type == "backward":
                member_chart.add(u"{0}'s tasks backward movements".format(member_name), backward_movements)

        except MemberReport.DoesNotExist:
            pass

    return member_chart.render_django_response()


# Spent time by week by member
def spent_time_by_week(current_user, week_of_year=None, board=None):
    if week_of_year is None:
        now = timezone.now()
        today = now.date()
        week_of_year_ = DailySpentTime.get_iso_week_of_year(today)
        week_of_year = "{0}W{1}".format(today.year, week_of_year_)

    y, w = week_of_year.split("W")
    week = Week(int(y), int(w))
    start_of_week = week.monday()
    end_of_week = week.sunday()

    chart_title = u"Spent time in week {0} ({1} - {2})".format(week_of_year,
                                                               start_of_week.strftime("%Y-%m-%d"),
                                                               end_of_week.strftime("%Y-%m-%d"))
    if board:
        chart_title += u" for board {0}".format(board.name)

    spent_time_chart = pygal.HorizontalBar(title=chart_title, legend_at_bottom=True, print_values=True,
                                           print_zeroes=False, human_readable=True)

    report_filter = {"date__year": y, "week_of_year": w}
    if board:
        report_filter["board_id"] = board.id

    team_spent_time = 0

    if board is None:
        boards = get_user_boards(current_user)
    else:
        boards = [board]
    members = Member.objects.filter(boards__in=boards, is_developer=True).distinct()
    for member in members:
        member_name = member.trello_username
        daily_spent_times = member.daily_spent_times.filter(**report_filter)
        spent_time = daily_spent_times.aggregate(Sum("spent_time"))["spent_time__sum"]
        if spent_time is None:
            spent_time = 0
        team_spent_time += spent_time

        if spent_time > 0:
            spent_time_chart.add(u"{0}'s spent time".format(member_name), spent_time)

    spent_time_chart.add(u"Team spent time", team_spent_time)

    return spent_time_chart.render_django_response()


# Evolution of spent time by member
def spent_time_by_week_evolution(board):
    chart_title = u"Evolution of each member's spent time by week"
    chart_title += u" for board {0} (fetched on {1})".format(board.name, board.get_human_fetch_datetime())

    evolution_chart = pygal.Line(title=chart_title, legend_at_bottom=True, print_values=True,
                                  print_zeroes=False, fill=False,
                                  human_readable=True, x_label_rotation=45)

    start_working_date = board.get_working_start_date()
    if start_working_date is None:
        return evolution_chart.render_django_response()

    end_working_date = board.get_working_end_date()
    if end_working_date is None:
        return evolution_chart.render_django_response()

    start_week = DailySpentTime.get_iso_week_of_year(start_working_date)
    end_week = DailySpentTime.get_iso_week_of_year(end_working_date)

    members = board.members.filter(is_developer=True)

    member_values = {member.id:[] for member in members}
    member_values["all"] = []

    x_labels = []

    week_i = copy.deepcopy(start_week)
    year_i = start_working_date.year
    while year_i < end_working_date.year or (year_i == end_working_date.year and week_i < end_week):

        there_is_data = board.daily_spent_times.filter(date__year=year_i, week_of_year=week_i).exists()
        if there_is_data:
            x_labels.append(u"{0}W{1}".format(year_i, week_i))

            team_spent_time = 0
            for member in members:
                daily_spent_times = member.daily_spent_times.filter(date__year=year_i, week_of_year=week_i)
                spent_time = daily_spent_times.aggregate(Sum("spent_time"))["spent_time__sum"]
                if spent_time is None:
                    spent_time = 0
                team_spent_time += spent_time

                if spent_time > 0:
                    member_values[member.id].append(spent_time)

            member_values["all"].append(team_spent_time)

        week_i += 1
        if week_i > number_of_weeks_of_year(year_i):
            week_i = 1
            year_i += 1

    evolution_chart.x_labels = x_labels
    for member in members:
        evolution_chart.add(member.trello_username, member_values[member.id])

    evolution_chart.add("All", member_values["all"])

    return evolution_chart.render_django_response()