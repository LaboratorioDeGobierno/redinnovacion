# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20170103_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='status', choices=[(0, 'Pendiente'), (1, 'Aceptado'), (2, 'Rechazado')]),
        ),
    ]
