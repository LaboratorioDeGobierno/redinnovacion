# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0014_auto_20171005_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentationtag',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, null=True, verbose_name='slug'),
        ),
    ]
