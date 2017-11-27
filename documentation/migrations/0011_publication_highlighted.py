# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0010_auto_20171004_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='highlighted',
            field=models.BooleanField(default=False, verbose_name='highlighted'),
        ),
    ]
