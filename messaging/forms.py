# -*- coding: utf-8 -*-
""" Forms for the notifications application. """
# standard library

# django

# models
from .models import EmailMessage

# views
from base.forms import BaseModelForm


class EmailMessageForm(BaseModelForm):
    """
    Form EmailMessage model.
    """

    class Meta:
        model = EmailMessage
        fields = (
            'to_user',
            'message',
        )
