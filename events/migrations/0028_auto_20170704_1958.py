# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0027_auto_20170622_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='creator',
            field=models.ForeignKey(related_name='created_events', on_delete=django.db.models.deletion.SET_NULL, verbose_name='creator', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='manager',
            field=models.ForeignKey(related_name='events_event_manager', on_delete=django.db.models.deletion.SET_NULL, verbose_name='manager', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
