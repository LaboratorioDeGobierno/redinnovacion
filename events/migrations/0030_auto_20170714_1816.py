# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0029_event_certification_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='certification_text',
            field=models.TextField(default=b'', verbose_name='certification text', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='google_maps_iframe',
            field=models.TextField(default=b'', verbose_name='google maps iframe', blank=True),
        ),
    ]
