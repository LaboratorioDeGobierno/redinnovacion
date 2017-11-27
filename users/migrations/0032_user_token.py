# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_userprofile_imported'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.CharField(default=b'', help_text=b"A token that can be used to verify the user's email", max_length=30, verbose_name='token', blank=True),
        ),
    ]
