# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0008_mailing_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='waiting_to_be_sent',
            field=models.BooleanField(default=True),
        ),
    ]
