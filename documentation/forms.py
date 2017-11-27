# -*- coding: utf-8 -*-
""" Forms for the newsletters application. """
# standard library

# django
from django import forms
from django.utils.translation import ugettext_lazy as _

# models
from .models import DocumentationFile
from .models import Methodology
from .models import Publication
from .models import Tool

# views
from base.forms import BaseModelForm


class DocumentationFileForm(BaseModelForm):
    """
    Form DocumentationFile model.
    """

    class Meta:
        model = DocumentationFile
        fields = "__all__"


class DocumentationTagsForm(forms.Form):
    """
    Form DocumentationTag.
    """
    tags = forms.CharField(
        required=False,
        label=_('Tags'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('add tags separated by commas')
            }
        )
    )


class MethodologyForm(BaseModelForm):
    """
    Form Methodology model.
    """

    class Meta:
        model = Methodology
        exclude = ('documentation_file', 'tags')


class PublicationForm(BaseModelForm):
    """
    Form Publication model.
    """

    class Meta:
        model = Publication
        exclude = ('documentation_file', 'tags')


class ToolForm(BaseModelForm):
    """
    Form Tool model.
    """

    class Meta:
        model = Tool
        exclude = ('documentation_file', 'tags')
