# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def forwards_func(apps, schema_editor):
    Activity = apps.get_model("activities", "Activity")
    db_alias = schema_editor.connection.alias
    Activity.objects.using(db_alias).filter(event__isnull=True).delete()


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0012_auto_20170531_0805'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
