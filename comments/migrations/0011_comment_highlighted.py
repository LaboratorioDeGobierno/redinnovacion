# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0010_auto_20170830_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='highlighted',
            field=models.BooleanField(default=False, verbose_name='highlighted'),
        ),
    ]
