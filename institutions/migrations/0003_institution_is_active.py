# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0002_auto_20170103_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
    ]
