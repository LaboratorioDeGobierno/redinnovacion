# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0009_auto_20170530_0524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivity',
            name='activity',
            field=models.ForeignKey(verbose_name='activity', to='activities.Activity'),
        ),
    ]
