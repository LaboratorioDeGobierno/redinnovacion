# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='archive',
            field=models.ForeignKey(related_name='cases', verbose_name='archive', blank=True, to='documents.File', null=True),
        ),
    ]
