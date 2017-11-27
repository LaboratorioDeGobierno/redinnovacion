# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_remove_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.PositiveIntegerField(null=True, verbose_name='phone'),
        ),
    ]
