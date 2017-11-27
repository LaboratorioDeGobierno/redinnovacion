# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0003_institution_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institution',
            name='phone'
        ),
        migrations.AddField(
            model_name='institution',
            name='phone',
            field=models.PositiveSmallIntegerField(verbose_name='phone', null=True),
        ),
    ]
