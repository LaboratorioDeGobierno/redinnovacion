# -*- coding: utf-8 -*-
""" Forms for the notifications application. """
# standard library

# django
from django import forms

# models
from .models import Notification

# views
from base.forms import BaseModelForm


class NotificationForm(BaseModelForm):
    """
    Form Notification model.
    """

    class Meta:
        model = Notification
        exclude = ()
