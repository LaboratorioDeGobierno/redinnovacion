# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_auto_20170531_0723'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='place',
            field=models.CharField(default=b'', max_length=255, verbose_name='place'),
        ),
        migrations.AlterField(
            model_name='event',
            name='address',
            field=models.CharField(max_length=255, verbose_name='address'),
        ),
    ]
