# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20170530_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]
