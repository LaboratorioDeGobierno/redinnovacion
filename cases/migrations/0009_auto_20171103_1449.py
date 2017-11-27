# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0008_case_editor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='publication_date',
        ),
        migrations.AddField(
            model_name='case',
            name='year',
            field=models.PositiveIntegerField(default=2017, verbose_name='year'),
        ),
    ]
