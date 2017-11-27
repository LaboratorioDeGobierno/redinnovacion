# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0006_auto_20170207_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='phone',
            field=models.PositiveIntegerField(null=True, verbose_name='phone'),
        ),
    ]
