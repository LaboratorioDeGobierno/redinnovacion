# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_auto_20170320_1239'),
        ('mailing', '0007_auto_20170226_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='event',
            field=models.ForeignKey(related_name='mailing', blank=True, to='events.Event', null=True),
        ),
    ]
