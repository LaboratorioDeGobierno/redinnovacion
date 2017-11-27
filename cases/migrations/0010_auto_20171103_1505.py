# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0023_documentationfile_hash_id'),
        ('cases', '0009_auto_20171103_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='methodologies',
        ),
        migrations.AddField(
            model_name='case',
            name='tools',
            field=models.ManyToManyField(to='documentation.Tool', verbose_name='tools', blank=True),
        ),
    ]
