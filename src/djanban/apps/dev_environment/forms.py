# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.forms import models
from django import forms
from django.utils import timezone

from djanban.apps.charts.models import CachedChart
from djanban.apps.dev_environment.models import Interruption, NoiseMeasurement


# Form to create a new interruption
class NewInterruptionForm(models.ModelForm):
    class Meta:
        model = Interruption
        fields = ["board", "interrupted_task", "cause", "spent_time", "comments"]

    def save(self, commit=True):
        super(NewInterruptionForm, self).save(commit=False)
        if commit:
            self.instance.datetime = timezone.now()
            self.instance.save()
            CachedChart.objects.filter(uuid__startswith="interruptions").delete()
        return self.instance


class DeleteInterruptionForm(forms.Form):
    confirmed = forms.BooleanField(label=u"Confirm you want to delete this interruption")


# Form to create a new noise measurement
class NewNoiseMeasurementForm(models.ModelForm):
    class Meta:
        model = NoiseMeasurement
        fields = ["noise_level", "subjective_noise_level", "comments"]

    def save(self, commit=True):
        super(NewNoiseMeasurementForm, self).save(commit=False)
        if commit:
            self.instance.datetime = timezone.now()
            self.instance.save()
            CachedChart.objects.filter(uuid__startswith="noise_measurement").delete()
        return self.instance


class DeleteNoiseMeasurementForm(forms.Form):
    confirmed = forms.BooleanField(label=u"Confirm you want to delete this noise measurement")