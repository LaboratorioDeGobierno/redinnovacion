# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20170307_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='experts',
            field=models.ManyToManyField(related_name='events_event_experts', verbose_name='experts', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='files',
            field=models.ManyToManyField(related_name='events_event_files', verbose_name='files', to='documents.File', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='institutions',
            field=models.ManyToManyField(related_name='events_event_institutions', verbose_name='institutions', to='institutions.Institution', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(related_name='events_event_participants', verbose_name='participants', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='photos',
            field=models.ManyToManyField(related_name='events_event_photos', verbose_name='photos', to='documents.Photo', blank=True),
        ),
    ]
