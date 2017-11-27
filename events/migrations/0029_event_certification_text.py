# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0028_auto_20170704_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='certification_text',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
