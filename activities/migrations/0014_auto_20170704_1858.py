# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0013_delete_orphan_activities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='event',
            field=models.ForeignKey(verbose_name='event', to='events.Event'),
        ),
    ]
