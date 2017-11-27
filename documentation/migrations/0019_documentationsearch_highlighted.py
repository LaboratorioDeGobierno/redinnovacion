# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0018_auto_20171011_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentationsearch',
            name='highlighted',
            field=models.BooleanField(default=False, verbose_name='highlighted'),
        ),
    ]
