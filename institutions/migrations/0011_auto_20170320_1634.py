# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0010_auto_20170320_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='url',
            field=models.URLField(null=True, verbose_name='url', blank=True),
        ),
    ]
