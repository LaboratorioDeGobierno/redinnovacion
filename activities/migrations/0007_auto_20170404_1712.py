# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0006_auto_20170331_1817'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useractivity',
            options={},
        ),
        migrations.AlterField(
            model_name='activity',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='event', to='events.Event', null=True),
        ),
    ]
