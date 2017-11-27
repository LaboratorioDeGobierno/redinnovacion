# -*- coding: utf-8 -*-
#
# models
from documents.models import Photo
from documents.models import File

# forms
from base.forms import BaseModelForm


class PhotoForm(BaseModelForm):
    class Meta:
        model = Photo
        fields = ('photo',)


class FileForm(BaseModelForm):
    class Meta:
        model = File
        fields = ('archive',)


class AttachmentForm(BaseModelForm):
    class Meta:
        model = File
        fields = '__all__'
