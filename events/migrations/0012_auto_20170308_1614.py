# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_event_acreditation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='acreditation',
            field=models.BooleanField(default=False, verbose_name='acreditation'),
        ),
    ]
