# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0034_auto_20170522_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='charge',
            field=models.CharField(max_length=150, null=True, verbose_name='charge'),
        ),
    ]
