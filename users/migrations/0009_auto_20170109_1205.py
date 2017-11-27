# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20170109_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='institution',
            field=models.ForeignKey(related_name='users', on_delete=django.db.models.deletion.SET_NULL, verbose_name='institution', to='institutions.Institution', null=True),
        ),
    ]
