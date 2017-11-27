# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0043_auto_20170613_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='institution',
            field=models.ForeignKey(related_name='users', on_delete=django.db.models.deletion.SET_NULL, verbose_name='institution', blank=True, to='institutions.Institution', null=True),
        ),
    ]
