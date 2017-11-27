# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0012_auto_20170629_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='use_only_active_users',
            field=models.BooleanField(default=False),
        ),
    ]
