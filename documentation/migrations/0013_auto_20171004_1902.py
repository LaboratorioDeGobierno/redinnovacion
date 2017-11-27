# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0012_methodology_tools'),
    ]

    operations = [
        migrations.AlterField(
            model_name='methodology',
            name='documentation_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='documentation file', blank=True, to='documentation.DocumentationFile', null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='documentation_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='documentation file', blank=True, to='documentation.DocumentationFile', null=True),
        ),
        migrations.AlterField(
            model_name='tool',
            name='documentation_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='documentation file', blank=True, to='documentation.DocumentationFile', null=True),
        ),
    ]
