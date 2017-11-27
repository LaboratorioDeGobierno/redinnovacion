# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_auto_20170206_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.PositiveIntegerField(null=True, verbose_name='phone', validators=[django.core.validators.MinLengthValidator(7)]),
        ),
    ]
