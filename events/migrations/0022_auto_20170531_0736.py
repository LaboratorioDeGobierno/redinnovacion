# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_auto_20170531_0725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name='final date'),
        ),
        migrations.AlterField(
            model_name='stage',
            name='start_date',
            field=models.DateTimeField(null=True, verbose_name='start date'),
        ),
    ]
