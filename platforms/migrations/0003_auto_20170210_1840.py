# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0002_auto_20170209_1817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userplatformattribute',
            name='attribute_name',
        ),
        migrations.RemoveField(
            model_name='userplatformattribute',
            name='attribute_value',
        ),
        migrations.AddField(
            model_name='userplatformattribute',
            name='name',
            field=models.CharField(default='asd', max_length=255, verbose_name='name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userplatformattribute',
            name='value',
            field=models.CharField(default='dsa', max_length=255, verbose_name='value'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='platform',
            name='name',
            field=models.CharField(unique=True, max_length=255, verbose_name='name'),
        ),
    ]
