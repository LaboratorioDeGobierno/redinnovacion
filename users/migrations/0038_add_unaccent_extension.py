# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from django.contrib.postgres.operations import UnaccentExtension


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0037_auto_20170524_1043'),
    ]

    operations = [
        UnaccentExtension(),
    ]
