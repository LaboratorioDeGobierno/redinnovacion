# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base.models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0033_auto_20170519_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=base.models.file_path, null=True, verbose_name='avatar', blank=True),
        ),
    ]
