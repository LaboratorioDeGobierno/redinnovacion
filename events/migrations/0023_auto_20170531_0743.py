# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_auto_20170531_0736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='google_maps_iframe',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
