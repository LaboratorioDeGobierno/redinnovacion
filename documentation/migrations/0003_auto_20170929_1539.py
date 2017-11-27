# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base.models
import django.db.models.deletion
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0002_auto_20170926_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('title', models.CharField(default=b'', max_length=255, verbose_name='title')),
                ('archive', models.FileField(upload_to=base.models.file_path, verbose_name='archive')),
                ('logo', easy_thumbnails.fields.ThumbnailerImageField(upload_to=base.models.file_path, null=True, verbose_name='logo', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('title', models.CharField(default=b'', max_length=255, verbose_name='title')),
                ('about', models.TextField(default=b'', verbose_name='about')),
                ('description', models.TextField(default=b'', verbose_name='description')),
                ('how_to_use', models.TextField(default=b'', verbose_name='how to use')),
                ('what_you_need', models.TextField(default=b'', verbose_name='what you need')),
                ('download_file', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='download file', blank=True, to='documentation.DownloadFile', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Documentation',
        ),
    ]
