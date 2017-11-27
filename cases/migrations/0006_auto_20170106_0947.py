# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0005_auto_20170105_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='archive',
            field=models.ForeignKey(related_name='cases', on_delete=django.db.models.deletion.SET_NULL, verbose_name='archive', to='documents.File', null=True),
        ),
    ]
