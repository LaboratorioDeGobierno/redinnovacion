# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='region',
            options={'ordering': ('order',), 'verbose_name': 'region', 'verbose_name_plural': 'regions'},
        ),
        migrations.AddField(
            model_name='region',
            name='order',
            field=models.IntegerField(unique=True, null=True),
        ),
    ]
