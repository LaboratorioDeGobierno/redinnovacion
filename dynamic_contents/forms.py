# -*- coding: utf-8 -*-
""" Forms for the dynamic_contents application. """
# standard library

# django

# models
from .models import DynamicContent

# views
from base.forms import BaseModelForm


class DynamicContentForm(BaseModelForm):
    """
    Form DynamicContent model.
    """

    class Meta:
        model = DynamicContent
        exclude = (
            'created_by',
            'methodology',
            'tool',
            'photos',
            'name',
        )

        fields = (
            'kind',
            'url',
            'content',
            'order'
        )
