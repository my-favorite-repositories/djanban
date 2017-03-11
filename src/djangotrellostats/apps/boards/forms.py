# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import

from crequest.middleware import CrequestMiddleware
from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import models
from django.utils import timezone

from djangotrellostats.apps.boards.models import Board, Card, List, Label
from djangotrellostats.apps.fetch.fetchers.trello.boards import Initializer
from djangotrellostats.apps.members.models import MemberRole
from djangotrellostats.remote_backends.factory import RemoteBackendConnectorFactory

from djangotrellostats.utils.custom_uuid import custom_uuid
from djangotrellostats.utils.week import get_iso_week_of_year


# Board edition form
class EditBoardForm(models.ModelForm):
    class Meta:
        model = Board
        fields = [
            "has_to_be_fetched", "comments", "estimated_number_of_hours",
            "percentage_of_completion", "hourly_rates",
            "enable_public_access", "public_access_code", "show_on_slideshow",
            "background_color", "title_color", "header_image"
        ]

    def __init__(self, *args, **kwargs):
        super(EditBoardForm, self).__init__(*args, **kwargs)
        self.fields["hourly_rates"].help_text = u"Please, select the hourly rates this board uses. System does not " \
                                                u"check if there is overlapping, so take care."

        self.fields["background_color"].widget.attrs["class"] = "jscolor"
        self.fields["title_color"].widget.attrs["class"] = "jscolor"

    def clean_background_color(self):
        try:
            int(self.cleaned_data.get("background_color"), 16)
        except ValueError:
            raise ValidationError("Background color is not an hexadecimal number")
        return self.cleaned_data.get("background_color")

    def clean_title_color(self):
        try:
            int(self.cleaned_data.get("title_color"), 16)
        except ValueError:
            raise ValidationError("Title color is not an hexadecimal number")
        return self.cleaned_data.get("title_color")

    def clean(self):
        cleaned_data = super(EditBoardForm, self).clean()
        return cleaned_data


# Board creation form
class NewBoardForm(models.ModelForm):
    MAX_NUM_LISTS = 20

    class Meta:
        model = Board
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super(NewBoardForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(NewBoardForm, self).clean()
        return cleaned_data

    def save(self, commit=True):
        if commit:
            with transaction.atomic():
                # Getting the current member (current user)
                current_request = CrequestMiddleware.get_request()
                current_user = current_request.user
                if not hasattr(current_user, "member"):
                    raise AssertionError("Only members can create lists")
                current_member = current_user.member

                connector = RemoteBackendConnectorFactory.factory(current_member)
                self.instance = connector.new_board(self.instance)
                self.instance.creator = current_member
                super(NewBoardForm, self).save(commit=True)

                # Adding the creator as admin of the board
                self.instance.members.add(current_member)
                role, created = MemberRole.objects.get_or_create(board=self.instance, type="admin")
                role.members.add(self.instance.creator)
                self.instance.roles.add(role)


# New list form
class NewListForm(models.ModelForm):
    class Meta:
        model = List
        fields = ["name", "type", "wip_limit"]

    def save(self, commit=True):
        if commit:
            with transaction.atomic():
                # Getting the current member (current user)
                current_request = CrequestMiddleware.get_request()
                current_user = current_request.user
                if not hasattr(current_user, "member"):
                    raise AssertionError("Only members can create lists")

                current_member = current_user.member
                list_ = self.instance

                self.instance = self.instance.board.new_list(current_member, self.instance)

                # Create the list
                super(NewListForm, self).save(commit=True)

                # Clean cached charts for this lists' board
                list_.board.clean_cached_charts()


class EditListForm(models.ModelForm):
    class Meta:
        model = List
        fields = ["name", "type", "wip_limit"]

    def __init__(self, *args, **kwargs):
        super(EditListForm, self).__init__(*args, **kwargs)
        current_list = self.instance
        lists = current_list.board.lists.order_by("position")

        if lists.exists():
            self.fields["list_to_be_swapped_with"] = models.ChoiceField(
                label="Swap this list position with",
                choices=[(list_i.id, list_i.name) for list_i in lists],
                required=True
            )
            self.fields["list_to_be_swapped_with"].initial = current_list.id

    def save(self, commit=True):
        if commit:
            with transaction.atomic():
                # Getting the current member (current user)
                current_request = CrequestMiddleware.get_request()
                current_user = current_request.user
                if not hasattr(current_user, "member"):
                    raise AssertionError("Only members can edit lists")

                current_member = current_user.member

                board = self.instance.board

                # Position of the list
                # Should we have to swap the list with any other?
                if self.cleaned_data.get("list_to_be_swapped_with") is not None\
                        and self.cleaned_data.get("list_to_be_swapped_with") != self.instance.id:
                    list_to_be_swapped_with_id = self.cleaned_data.get("list_to_be_swapped_with")
                    list_to_be_swapped_with = board.lists.get(id=list_to_be_swapped_with_id)
                    list_to_be_swapped_with_position = list_to_be_swapped_with.position
                    list_to_be_swapped_with.position = self.instance.position
                    self.instance.position = list_to_be_swapped_with_position
                    list_to_be_swapped_with.save()

                self.instance = board.edit_list(current_member, self.instance)

                # Edit the list
                super(EditListForm, self).save(commit=True)

                # Clean cached charts for this lists' board
                self.instance.board.clean_cached_charts()


# New card
class NewCardForm(models.ModelForm):
    class Meta:
        model = Card
        fields = ["name", "description", "list", "labels"]

    def __init__(self, *args, **kwargs):
        super(NewCardForm, self).__init__(*args, **kwargs)
        board = self.instance.board

        # Only list of the same board are choices
        lists = board.lists.exclude(type="closed").order_by("position")
        self.fields["list"].choices = [(list_.id, list_.name) for list_ in lists]

        # Only labels of the same board are choices
        labels = board.labels.exclude(name="").order_by("name")
        self.fields["labels"].choices = [(label.id, label.name) for label in labels]

    def save(self, commit=True):
        if commit:
            with transaction.atomic():
                board = self.instance.board
                list_ = self.instance.list

                # Getting the current member (current user)
                current_request = CrequestMiddleware.get_request()
                current_user = current_request.user
                if not hasattr(current_user, "member"):
                    raise AssertionError("Only members can create lists")

                current_member = current_user.member
                self.instance = list_.add_card(current_member, self.instance.name, position="bottom")

                self.instance.creation_datetime = timezone.now()
                self.instance.last_activity_datetime = timezone.now()
                # Create the card
                super(NewCardForm, self).save(commit=True)
                # Clean cached charts for this board
                board.clean_cached_charts()


class LabelForm(models.ModelForm):
    class Meta:
        model = Label
        fields = ["name", "color"]

    def __init__(self, *args, **kwargs):
        super(LabelForm, self).__init__(*args, **kwargs)

        self.fields["color"].widget.attrs["class"] = "jscolor"

    def clean_color(self):
        try:
            int(self.cleaned_data.get("color"), 16)
        except ValueError:
            raise ValidationError("This color is not an hexadecimal number")
        return self.cleaned_data.get("color")


# Week summary filter
# This filter filters the
class WeekSummaryFilterForm(forms.Form):
    year = forms.ChoiceField(label="Year", choices=[], required=True)
    week = forms.ChoiceField(label="Week", choices=[], required=True)
    member = forms.ChoiceField(label="Member", choices=[], required=True)

    def __init__(self, board, post_data=None, initial=None):
        super(WeekSummaryFilterForm, self).__init__(data=post_data, initial=initial)
        now = timezone.now()
        year = now.year

        working_start_date = board.get_working_start_date()
        working_end_date = board.get_working_end_date()
        if working_start_date and working_end_date:
            self.fields["year"].choices = [(year_i, year_i) for year_i in range(working_start_date.year, working_end_date.year+1)]

            if working_start_date.year == working_end_date.year:
                start_week = get_iso_week_of_year(working_start_date)
                end_week = get_iso_week_of_year(working_end_date)
                self.fields["week"].choices = [(week_i, week_i) for week_i in range(start_week, end_week+1)]
            else:
                self.fields["week"].choices = [(week_i, week_i) for week_i in range(1, 53 + 1)]
        else:
            self.fields["year"].choices = [(year_i, year_i) for year_i in range(year-100, year+101)]
            self.fields["week"].choices = [(week_i, week_i) for week_i in range(1, 53+1)]

        self.fields["member"].choices = [("all", "All")] +\
            [(member.id, member.external_username) for member in board.members.filter(is_developer=True)]

        if initial is None:
            self.initial["year"] = year
            self.initial["week"] = get_iso_week_of_year(now)
            self.initial["member"] = "all"
