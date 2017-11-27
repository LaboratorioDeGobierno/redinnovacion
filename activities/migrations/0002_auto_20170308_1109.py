# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='address',
            field=models.CharField(max_length=50, null=True, verbose_name='address', blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name='final date', blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='manager',
            field=models.ForeignKey(related_name='activities_activity_manager', verbose_name='manager', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='quota',
            field=models.IntegerField(null=True, verbose_name='quota', blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='start_date',
            field=models.DateTimeField(null=True, verbose_name='start date', blank=True),
        ),
    ]
