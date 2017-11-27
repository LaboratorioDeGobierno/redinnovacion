# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_userevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userevent',
            name='event',
            field=models.ForeignKey(verbose_name='event', to='events.Event'),
        ),
    ]
