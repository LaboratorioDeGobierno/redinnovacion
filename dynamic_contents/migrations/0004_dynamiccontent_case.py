# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0008_case_editor'),
        ('dynamic_contents', '0003_auto_20171024_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='dynamiccontent',
            name='case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='cases.Case', null=True),
        ),
    ]
