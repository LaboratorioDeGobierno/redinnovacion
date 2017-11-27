# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interests', '0001_initial'),
        ('users', '0010_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='interests',
            field=models.ManyToManyField(related_name='users', verbose_name='interests', to='interests.Interest'),
        ),
    ]
