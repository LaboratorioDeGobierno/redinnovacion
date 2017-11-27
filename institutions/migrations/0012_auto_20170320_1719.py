# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base.models
import phonenumber_field.modelfields
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0011_auto_20170320_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='address',
            field=models.CharField(max_length=50, null=True, verbose_name='address', blank=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='logo',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=base.models.file_path, null=True, verbose_name='logo', blank=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, verbose_name='phone', blank=True),
        ),
    ]
