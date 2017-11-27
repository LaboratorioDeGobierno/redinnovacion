# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0006_auto_20170606_0745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='activities.Activity', null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='events.Event', null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='comments.Comment', null=True),
        ),
    ]
