# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
        ('users', '0003_auto_20170103_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='institutions',
            field=models.ManyToManyField(to='institutions.Institution', verbose_name='institutions'),
        ),
    ]
