# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evaluations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventevaluation',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='activities.Activity', null=True),
        ),
    ]
