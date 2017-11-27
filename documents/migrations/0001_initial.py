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
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('archive', models.FileField(upload_to=b'', verbose_name='archive')),
                ('description', models.TextField(verbose_name='description')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('photo', easy_thumbnails.fields.ThumbnailerImageField(upload_to=base.models.file_path, verbose_name='image')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
