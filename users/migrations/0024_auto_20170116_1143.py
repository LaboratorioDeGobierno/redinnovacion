# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_auto_20170112_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='region',
            field=models.ForeignKey(related_name='users', on_delete=django.db.models.deletion.SET_NULL, verbose_name='region', to='regions.Region', null=True),
        ),
    ]
