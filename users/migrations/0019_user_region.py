# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '__first__'),
        ('users', '0018_auto_20170112_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='region',
            field=models.ForeignKey(related_name='users', verbose_name='region', to='regions.Region', null=True),
        ),
    ]
