# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0005_auto_20170929_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='downloadfile',
            name='name',
            field=models.CharField(default=b'', max_length=255, verbose_name='name file'),
        ),
    ]
