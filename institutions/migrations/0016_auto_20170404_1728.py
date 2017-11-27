# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0015_auto_20170404_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='slug', max_length=100),
        ),
    ]
