# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import base.models


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0002_auto_20170530_0547'),
        ('events', '0018_auto_20170530_0858'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='county', blank=True, to='regions.County', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='google_maps_iframe',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='presentation',
            field=models.FileField(null=True, upload_to=base.models.file_path, blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='quota',
            field=models.IntegerField(null=True, verbose_name='quota', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='region', blank=True, to='regions.Region', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.CharField(default=b'', max_length=255, verbose_name='tags'),
        ),
        migrations.AddField(
            model_name='event',
            name='what_does_it_consist_of',
            field=models.TextField(default=b'', verbose_name='\xbfEn qu\xe9 consiste el taller/tipo de actividad?'),
        ),
    ]
