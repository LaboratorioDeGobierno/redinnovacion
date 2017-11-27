# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# django
from django.db import migrations, models

# utils
from users.utils import calculate_slug

# enums
from users.enums import UserEnum


def reset_slug(apps, schema_editor):
    User = apps.get_model('users', 'User')
    # Reset slugs
    User.objects.all().update(slug=None)
    # generate slugs
    for user in User.objects.all():
        # check if the user is active in the system
        if user.is_active and user.status == UserEnum.STATUS_ACCEPTED:
            # calculate slug
            user.slug = calculate_slug(
                user.first_name,
                user.last_name,
                user.mother_family_name,
                user.email,
                User
            )
            user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0049_auto_20170811_1238'),
    ]

    operations = [
        migrations.RunPython(reset_slug)
    ]
