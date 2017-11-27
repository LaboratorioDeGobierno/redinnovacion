# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0002_auto_20170530_0547'),
        ('users', '0040_auto_20170530_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=255, null=True, verbose_name='address'),
        ),
        migrations.AddField(
            model_name='user',
            name='county',
            field=models.ForeignKey(related_name='users', on_delete=django.db.models.deletion.SET_NULL, verbose_name='county', to='regions.County', null=True),
        ),
    ]
