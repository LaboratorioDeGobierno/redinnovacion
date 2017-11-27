# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0005_auto_20170207_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='phone',
            field=models.PositiveIntegerField(null=True, verbose_name='phone', validators=[django.core.validators.MinLengthValidator(6)]),
        ),
    ]
