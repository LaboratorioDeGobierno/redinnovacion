# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0035_auto_20170522_1830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='description',
        ),
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(null=True, verbose_name='description'),
        ),
    ]
