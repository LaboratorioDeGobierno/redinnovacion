# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Project',
            new_name='Platform',
        ),
        migrations.RenameField(
            model_name='userplatformattribute',
            old_name='project',
            new_name='platform',
        ),
    ]
