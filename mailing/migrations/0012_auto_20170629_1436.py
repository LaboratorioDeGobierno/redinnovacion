# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0011_auto_20170323_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='event',
            field=models.ForeignKey(related_name='mailing', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='events.Event', null=True),
        ),
    ]
