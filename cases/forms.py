# -*- coding: utf-8 -*-
""" Forms for the newsletters application. """
# standard library

# django
from django import forms
from django.utils.translation import ugettext_lazy as _

# models
from cases.models import Case

# forms
from base.forms import BaseModelForm


class CaseTagsForm(forms.Form):
    """
    Form CaseTag.
    """
    tags = forms.CharField(
        required=False,
        label=_('tags'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('add tags separated by commas')
            }
        )
    )


class CaseForm(BaseModelForm):
    """
    Form Case model.
    """

    class Meta:
        model = Case
        exclude = ('author', 'editor', 'attachments', 'tags')
