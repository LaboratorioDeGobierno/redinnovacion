# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0002_auto_20170103_1604'),
        ('users', '0007_user_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='institutions',
        ),
        migrations.AddField(
            model_name='user',
            name='institution',
            field=models.ForeignKey(related_name='users', verbose_name='institution', to='institutions.Institution', null=True),
        ),
    ]
