import re
from django.db import models

from base.models import BaseModel, file_path
from django.utils.translation import ugettext_lazy as _

from easy_thumbnails.fields import ThumbnailerImageField


class File(BaseModel):
    title = models.CharField(
        _('title'),
        max_length=255,
        default='',
    )
    archive = models.FileField(
        _('archive'),
        upload_to=file_path,
    )
    description = models.TextField(
        _('description'),
        default='',
    )

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ''

    def get_filename(self):
        """
        Returns the name of the file uploaded trimming path characters,
        handling whitespace and case.
        """
        paths = self.archive.name.split('/')
        filename = paths[-1]
        filename = re.sub(r'[_-]', ' ', filename)
        filename = filename[0].upper() + filename[1:]
        return filename


class Photo(BaseModel):
    title = models.CharField(
        _('title'),
        max_length=255,
        default='',
    )
    photo = ThumbnailerImageField(
        _('image'),
        upload_to=file_path,
    )

    def get_absolute_url(self):
        return ''
