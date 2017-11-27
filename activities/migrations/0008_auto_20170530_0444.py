# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '__first__'),
        ('activities', '0007_auto_20170404_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='city',
            field=models.CharField(max_length=50, null=True, verbose_name='city', blank=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='region',
            field=models.ForeignKey(verbose_name='region', blank=True, to='regions.Region', null=True),
        ),
    ]
