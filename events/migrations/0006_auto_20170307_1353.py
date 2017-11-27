# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_stage_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='description',
            field=models.TextField(null=True, verbose_name='description', blank=True),
        ),
        migrations.AlterField(
            model_name='stage',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name='final date', blank=True),
        ),
        migrations.AlterField(
            model_name='stage',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='name', blank=True),
        ),
        migrations.AlterField(
            model_name='stage',
            name='start_date',
            field=models.DateTimeField(null=True, verbose_name='start date', blank=True),
        ),
    ]
