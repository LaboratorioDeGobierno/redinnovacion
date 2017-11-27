# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0038_add_unaccent_extension'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='interests',
            field=models.ManyToManyField(related_name='users', verbose_name='interests', to='interests.Interest', blank=True),
        ),
    ]
