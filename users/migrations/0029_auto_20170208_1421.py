# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_auto_20170207_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.PositiveIntegerField(null=True, verbose_name='phone'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='time_in_ri',
            field=models.PositiveSmallIntegerField(default=None, null=True, verbose_name='time in ri', choices=[(0, 'Una vez a la semana'), (1, 'Una vez cada 15 d\xedas'), (2, 'Una vez al mes'), (3, 'Solo algunas veces ocasionales al a\xf1o'), (4, 'Otro')]),
        ),
    ]
