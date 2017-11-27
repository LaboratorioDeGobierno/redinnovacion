# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0049_auto_20170811_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_activity',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='The datetime of the last activity performed by the user', verbose_name='last activity'),
        ),
    ]
