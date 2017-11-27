# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20170308_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='acreditation',
            field=models.BooleanField(default=True, verbose_name='acreditation'),
        ),
    ]
