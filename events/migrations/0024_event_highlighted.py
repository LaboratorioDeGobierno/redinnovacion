# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0023_auto_20170531_0743'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='highlighted',
            field=models.BooleanField(default=False, verbose_name='highlighted'),
        ),
    ]
