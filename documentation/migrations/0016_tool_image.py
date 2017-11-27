# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base.models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0015_documentationtag_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=base.models.file_path, null=True, verbose_name='image', blank=True),
        ),
    ]
