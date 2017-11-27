# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0004_methodology_publication'),
    ]

    operations = [
        migrations.RenameField(
            model_name='downloadfile',
            old_name='title',
            new_name='name',
        ),
    ]
