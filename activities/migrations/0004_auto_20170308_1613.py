# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_useractivity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivity',
            name='stage',
            field=models.ForeignKey(verbose_name='stage', blank=True, to='events.Stage', null=True),
        ),
    ]
