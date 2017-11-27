# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_emailmessage_read'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailmessage',
            name='subject',
            field=models.CharField(max_length=255, null=True, verbose_name='subjet', blank=True),
        ),
    ]
