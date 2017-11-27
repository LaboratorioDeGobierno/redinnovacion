# -*- coding: utf-8 -*-
""" Forms for the newsletters application. """
# standard library

# django
from django import forms

# models
from .models import Newsletter

# views
from base.forms import BaseModelForm


class NewsletterForm(BaseModelForm):
    """
    Form Newsletter model.
    """

    class Meta:
        model = Newsletter
        exclude = (
            'comments',
        )
