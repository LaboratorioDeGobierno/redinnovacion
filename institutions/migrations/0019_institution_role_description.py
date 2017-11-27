# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0018_auto_20170519_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='role_description',
            field=models.TextField(max_length=500, null=True, verbose_name='role description', blank=True),
        ),
    ]
