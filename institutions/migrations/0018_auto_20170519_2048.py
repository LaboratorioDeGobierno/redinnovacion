# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0017_auto_20170512_1728'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='institution',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='institution',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, null=True, verbose_name='slug'),
        ),
    ]
