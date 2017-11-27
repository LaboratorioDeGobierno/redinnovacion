# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base.models
from django.conf import settings
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20170307_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='activity_type',
            field=models.CharField(max_length=50, null=True, verbose_name='type of activity', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name='final date', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='experts',
            field=models.ManyToManyField(related_name='events_event_experts', null=True, verbose_name='experts', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='files',
            field=models.ManyToManyField(related_name='events_event_files', null=True, verbose_name='files', to='documents.File', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='institutions',
            field=models.ManyToManyField(related_name='events_event_institutions', null=True, verbose_name='institutions', to='institutions.Institution', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='manager',
            field=models.ForeignKey(related_name='events_event_manager', verbose_name='manager', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(related_name='events_event_participants', null=True, verbose_name='participants', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='photos',
            field=models.ManyToManyField(related_name='events_event_photos', null=True, verbose_name='photos', to='documents.Photo', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='principal_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=base.models.file_path, null=True, verbose_name='principal image', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(null=True, verbose_name='start date', blank=True),
        ),
    ]
