# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.contrib.auth.hashers import make_password


def create_users(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    User = apps.get_model('users', 'User')

    User.objects.create(
        date_joined='2012-10-09T21:42:23Z',
        email='pablo@aulab.com',
        first_name='Pablo',
        is_active=True,
        is_staff=False,
        is_superuser=False,
        last_name='Minier',
        password=make_password('pablo'),
    )


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20170103_1519'),
    ]

    operations = [
        migrations.RunPython(create_users),
    ]
