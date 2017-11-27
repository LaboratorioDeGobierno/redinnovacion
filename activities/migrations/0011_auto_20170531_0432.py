# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0010_auto_20170530_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='event', blank=True, to='events.Event', null=True),
        ),
    ]
