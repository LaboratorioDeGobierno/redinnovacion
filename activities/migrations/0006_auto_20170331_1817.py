# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_auto_20170330_1713'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useractivity',
            options={'permissions': (('attend_useractivity', 'Can change attendance status'),)},
        ),
    ]
