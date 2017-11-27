# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0013_mailing_use_only_active_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='filter_by_user_status',
            field=models.PositiveSmallIntegerField(blank=True, null=True, choices=[(None, b''), (0, 'Pendiente'), (1, 'Aceptado'), (2, 'Rechazado'), (3, 'Otro')]),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='targets',
            field=models.ManyToManyField(to='mailing.EmailTarget', blank=True),
        ),
    ]
