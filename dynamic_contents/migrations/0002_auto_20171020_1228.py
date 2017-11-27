# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_contents', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dynamiccontent',
            name='value',
        ),
        migrations.AddField(
            model_name='dynamiccontent',
            name='content',
            field=models.TextField(null=True, verbose_name='content', blank=True),
        ),
        migrations.AddField(
            model_name='dynamiccontent',
            name='url',
            field=models.URLField(null=True, verbose_name='url', blank=True),
        ),
    ]
