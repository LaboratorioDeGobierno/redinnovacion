#!/usr/bin/env python
# -*- coding: utf-8 -*-

# django
from django import forms
from django.utils.translation import ugettext_lazy as _

# models
from .models import Activity
from events.models import Stage
from regions.models import Region

# base form
from base.forms import BaseModelForm


INSCRIPTION_STATE_CHOICES = (
    ("", "---------"),
    (Stage.STAGE_TYPE_INSCRIPTION, u"Inscrito"),
    (Stage.STAGE_TYPE_ACTIVITY, u"Acreditado"),
)


class ActivityForm(BaseModelForm):

    class Meta:
        model = Activity
        fields = (
            'name',
            'address',
            'start_date',
            'end_date',
            'description',
            'manager',
            'quota'
        )
        labels = {
            'name': u'Nombre de la actividad',
        }


class ActivityFilterForm(forms.Form):
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=u'Región'
    )
    activity = forms.ModelChoiceField(
        queryset=Activity.objects.all(),
        required=False,
        label=u'Actividad'
    )
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'datetime-picker form-control'}
        ),
        required=False,
        label=u'Fecha de inicio'
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'datetime-picker form-control'}
        ),
        required=False,
        label=u'Fecha de término'

    )
    inscription_state = forms.ChoiceField(
        choices=INSCRIPTION_STATE_CHOICES,
        required=False,
        label=u'Estado de inscripción'
    )

    def clean(self):
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")
        if end_date < start_date:
            msg = _("End date should be greater than start date.")
            self._errors["end_date"] = self.error_class([msg])
