# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_auto_20170404_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='activity_type',
            field=models.CharField(default=b'Workshop', max_length=50, verbose_name='type of activity', choices=[(b'Workshop', 'Workshop'), (b'Meeting', 'Meeting'), (b'Talk', 'Talk'), (b'Event', 'Event')]),
        ),
    ]
