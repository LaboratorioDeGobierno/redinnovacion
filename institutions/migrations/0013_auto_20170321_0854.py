# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0012_auto_20170320_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='address',
            field=models.CharField(max_length=255, null=True, verbose_name='address', blank=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
    ]
