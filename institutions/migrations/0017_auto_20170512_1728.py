# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0016_auto_20170404_1728'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='institution',
            unique_together=set([('name', 'address')]),
        ),
        migrations.RemoveField(
            model_name='institution',
            name='region',
        ),
    ]
