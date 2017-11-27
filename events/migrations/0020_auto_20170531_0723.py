# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_auto_20170530_1216'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stage',
            options={'ordering': ('start_date',)},
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=100, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='stage',
            name='stage_type',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Type Stage', choices=[(1, 'Convocatoria'), (2, 'Inscripcion'), (3, 'Acreditaci\xf3n'), (4, 'Actividad'), (5, 'Evaluaci\xf3n')]),
        ),
    ]
