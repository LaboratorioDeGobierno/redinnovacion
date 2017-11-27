# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import Group
from django.db import migrations, models


def create_experimenta_group(apps, schema_editor):
    Group.objects.get_or_create(name="Experimenta")


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0047_auto_20170714_2245'),
    ]

    operations = [
        migrations.RunPython(create_experimenta_group),
    ]
