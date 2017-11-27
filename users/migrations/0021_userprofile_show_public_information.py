# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_remove_userprofile_show_public_information'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='show_public_information',
            field=models.NullBooleanField(default=None, verbose_name='show public information', choices=[(False, 'No'), (True, 'Yes')]),
        ),
    ]
