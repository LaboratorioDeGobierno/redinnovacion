# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0008_auto_20170208_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='imported',
            field=models.BooleanField(default=False),
        ),
    ]
