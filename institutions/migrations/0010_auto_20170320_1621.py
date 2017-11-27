# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0009_institution_imported'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='institution',
            unique_together=set([('name', 'region')]),
        ),
    ]
