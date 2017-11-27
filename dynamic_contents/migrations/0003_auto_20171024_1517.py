# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_contents', '0002_auto_20171020_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamiccontent',
            name='methodology',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='documentation.Methodology', null=True),
        ),
        migrations.AlterField(
            model_name='dynamiccontent',
            name='tool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='documentation.Tool', null=True),
        ),
    ]
