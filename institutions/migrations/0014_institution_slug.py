# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0013_auto_20170321_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='slug',
            field=models.SlugField(verbose_name='slug', blank=True, max_length=100),
        ),
    ]
