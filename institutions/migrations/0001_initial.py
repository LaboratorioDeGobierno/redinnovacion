# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base.models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('url', models.URLField(verbose_name='url')),
                ('address', models.CharField(max_length=50, verbose_name='address')),
                ('phone', models.CharField(max_length=50, verbose_name='phone')),
                ('logo', easy_thumbnails.fields.ThumbnailerImageField(upload_to=base.models.file_path, verbose_name='logo')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
