# -*- coding: utf-8 -*-

import shortuuid

from djanban.apps.requirements.models import Requirement
from django import forms
from ckeditor.widgets import CKEditorWidget


# Requirement form
class RequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = ["code", "name", "description", "active", "other_comments", "value", "estimated_number_of_hours"]

    def __init__(self, *args, **kwargs):
        super(RequirementForm, self).__init__(*args, **kwargs)
        self.fields["description"].widget = CKEditorWidget()
        self.fields["other_comments"].widget = CKEditorWidget()


# New requirement form
class NewRequirementForm(RequirementForm):
    class Meta:
        model = Requirement
        fields = ["code", "name", "description", "active", "other_comments", "value", "estimated_number_of_hours"]

    def __init__(self, *args, **kwargs):
        super(NewRequirementForm, self).__init__(*args, **kwargs)
        self.initial["code"] = u"{0}{1}".format(self.instance.board.name[0].upper(),
                                                shortuuid.ShortUUID().random(length=4).upper())


# Edit requirement form
class EditRequirementForm(RequirementForm):
    class Meta:
        model = Requirement
        fields = ["name", "description", "active", "other_comments", "value", "estimated_number_of_hours"]


# Delete requirement form
class DeleteRequirementForm(forms.Form):
    confirmed = forms.BooleanField(label=u"Confirm you want to delete this requirement")
