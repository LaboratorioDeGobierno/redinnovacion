# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20170303_1251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stage',
            name='type_stage',
        ),
        migrations.AddField(
            model_name='stage',
            name='stage_type',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Type Stage', choices=[(1, 'Convocatoria'), (2, 'Inscripcion'), (3, 'Confirmacion'), (4, 'Acreditacion Evento'), (5, 'Acreditacion Actividad'), (6, 'Finalizada')]),
        ),
    ]
