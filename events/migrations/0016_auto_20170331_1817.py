# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_auto_20170331_1146'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userevent',
            options={'permissions': (('attend_userevent', 'Can change attendance status'),)},
        ),
    ]
