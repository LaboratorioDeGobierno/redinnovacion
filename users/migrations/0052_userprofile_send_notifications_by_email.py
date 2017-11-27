# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0051_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='send_notifications_by_email',
            field=models.BooleanField(default=True, verbose_name='send notifications by email'),
        ),
    ]
