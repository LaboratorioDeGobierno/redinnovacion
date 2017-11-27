# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
                ('start_date', models.DateTimeField(verbose_name='start date')),
                ('end_date', models.DateTimeField(null=True, verbose_name='final date')),
                ('type_stage', models.CharField(max_length=1, null=True, verbose_name='Type Stage', choices=[(1, b'Convocatoria'), (2, b'Inscripcion'), (3, b'Confirmacion'), (4, b'Acreditacion Evento'), (5, b'Acreditacion Actividad'), (6, b'Finalizada')])),
                ('event', models.ForeignKey(verbose_name='event', to='events.Event')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
