# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base.models
from django.conf import settings
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_auto_20170103_1633'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institutions', '0009_institution_imported'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
                ('address', models.CharField(max_length=50, verbose_name='address')),
                ('start_date', models.DateTimeField(verbose_name='start date')),
                ('end_date', models.DateTimeField(null=True, verbose_name='final date')),
                ('principal_image', easy_thumbnails.fields.ThumbnailerImageField(upload_to=base.models.file_path, verbose_name='principal image')),
                ('activity_type', models.CharField(max_length=50, verbose_name='type of activity')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('experts', models.ManyToManyField(related_name='events_event_experts', verbose_name='experts', to=settings.AUTH_USER_MODEL)),
                ('files', models.ManyToManyField(related_name='events_event_files', verbose_name='files', to='documents.File')),
                ('institutions', models.ManyToManyField(related_name='events_event_institutions', verbose_name='institutions', to='institutions.Institution')),
                ('manager', models.ForeignKey(related_name='events_event_manager', verbose_name='manager', to=settings.AUTH_USER_MODEL)),
                ('participants', models.ManyToManyField(related_name='events_event_participants', verbose_name='participants', to=settings.AUTH_USER_MODEL)),
                ('photos', models.ManyToManyField(related_name='events_event_photos', verbose_name='photos', to='documents.Photo')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
