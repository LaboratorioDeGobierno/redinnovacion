# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0003_auto_20170104_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='archive',
            field=models.ForeignKey(related_name='cases', verbose_name='archive', to='documents.File', null=True),
        ),
    ]
