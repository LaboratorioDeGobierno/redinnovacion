# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def remove_attributes(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    model = apps.get_model('platforms', 'UserPlatformAttribute')
    for attribute in model.objects.all():
        attribute.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0005_auto_20170213_1747'),
    ]

    operations = [
        migrations.RunPython(
            remove_attributes,
            reverse_code=lambda apps, schema_editor: None
        ),
        migrations.AlterUniqueTogether(
            name='userplatformattribute',
            unique_together=set([('user', 'platform', 'name')]),
        ),
    ]
