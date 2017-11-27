# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20170306_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
    ]
