# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0010_auto_20170323_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='mailing_process_started_at',
            field=models.DateTimeField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='mailing',
            name='scheduled_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
