# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_auto_20170208_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='imported',
            field=models.BooleanField(default=False),
        ),
    ]
