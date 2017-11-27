# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0004_auto_20170210_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform',
            name='token',
            field=models.CharField(max_length=255, verbose_name='token'),
        ),
    ]
