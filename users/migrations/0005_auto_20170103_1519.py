# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_institutions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='institutions',
            field=models.ManyToManyField(related_name='users', verbose_name='institutions', to='institutions.Institution'),
        ),
    ]
