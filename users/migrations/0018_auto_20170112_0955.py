# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='show_public_information',
            field=models.NullBooleanField(default=None, verbose_name='show public information', choices=[(False, 'No'), (True, 'Yes')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='time_in_ri',
            field=models.PositiveSmallIntegerField(default=None, null=True, verbose_name='time in ri', choices=[(0, 'Una vez a la semana'), (1, 'Una vez cada 15 d\xedas'), (2, 'Una vez al mes'), (3, 'Solo algunas veces ocasionales al a\xf1o')]),
        ),
    ]
