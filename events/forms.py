#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from base.forms import BaseModelForm
from events.models import Event
from events.models import Stage

from users.models import User


class EventForm(BaseModelForm):
    non_staff_exclude = (
        'activity_type',
        'manager',
        'quota',
        'tags',
        'highlighted',
        'google_maps_iframe',
        'presentation',
        'certification_text',
    )

    class Meta:
        model = Event
        fields = (
            'name',
            'activity_type',
            'address',
            'place',
            'manager',
            'quota',
            'region',
            'county',
            'tags',
            'highlighted',
            'google_maps_iframe',
            'description',
            'what_does_it_consist_of',
            'certification_text',
            'presentation',
        )
        labels = {
            'name': u'Nombre de la actividad',
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        self.fields['manager'].queryset = User.objects.filter(is_staff=True)

    def exclude_staff_fields(self):
        """
        Delete fields exclusive to administrators from a form instance
        """
        for key in getattr(self, 'non_staff_exclude', ()):
            del self.fields[key]


class StageForm(BaseModelForm):
    event = forms.Field(widget=forms.HiddenInput())

    class Meta:
        model = Stage
        fields = (
            'name',
            'start_date',
            'end_date',
            'stage_type',
            'description',
            'event',
        )
        labels = {
            'name': u'Nombre de la etapa',
        }


class EventStageForm(BaseModelForm):
    class Meta:
        model = Stage
        fields = (
            'start_date',
            'end_date',
            'is_active',
        )
        labels = {
            'start_date': u'Fecha y hora de inicio',
            'end_date': u'Fecha y hora de término',
            'is_active': u'Visible',
        }
