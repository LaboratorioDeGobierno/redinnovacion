# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0008_auto_20170530_0444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='manager',
            field=models.ForeignKey(related_name='activities_activity_manager', on_delete=django.db.models.deletion.SET_NULL, verbose_name='manager', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='region', blank=True, to='regions.Region', null=True),
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='stage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='stage', blank=True, to='events.Stage', null=True),
        ),
    ]
