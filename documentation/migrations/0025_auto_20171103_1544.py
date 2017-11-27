# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base.models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0024_auto_20171103_1518'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documentationfile',
            old_name='logo',
            new_name='image',
        ),

        migrations.AlterField(
            model_name='documentationfile',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=base.models.file_path, null=True, verbose_name='file image', blank=True),
        ),
    ]
