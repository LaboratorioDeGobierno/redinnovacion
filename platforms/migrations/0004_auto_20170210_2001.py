# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0003_auto_20170210_1840'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='platform',
            options={'ordering': ('name',), 'verbose_name': 'platform', 'verbose_name_plural': 'platforms'},
        ),
        migrations.AlterModelOptions(
            name='userplatformattribute',
            options={'verbose_name': 'user platform attribute', 'verbose_name_plural': 'user platform attributes'},
        ),
    ]
