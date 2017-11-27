# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '__first__'),
        ('institutions', '0004_auto_20170207_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='region',
            field=models.ForeignKey(related_name='institutions', on_delete=django.db.models.deletion.SET_NULL, verbose_name='region', to='regions.Region', null=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='phone',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='phone', validators=[django.core.validators.MinLengthValidator(7)]),
        ),
    ]
