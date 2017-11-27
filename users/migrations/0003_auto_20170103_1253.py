# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base.models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_initial_admin_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=50, null=True, verbose_name='address'),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=base.models.file_path, null=True, verbose_name='avatar'),
        ),
        migrations.AddField(
            model_name='user',
            name='charge',
            field=models.CharField(max_length=50, null=True, verbose_name='charge'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=50, null=True, verbose_name='phone'),
        ),
    ]
