# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_stage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='type_stage',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='Type Stage', choices=[(1, 'Convocatoria'), (2, 'Inscripcion'), (3, 'Confirmacion'), (4, 'Acreditacion Evento'), (5, 'Acreditacion Actividad'), (6, 'Finalizada')]),
        ),
    ]
