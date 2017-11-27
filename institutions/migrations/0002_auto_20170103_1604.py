# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_institutions(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Institution = apps.get_model('institutions', 'Institution')

    Institution.objects.create(
        name='Intitucion aulabri',
        url='www.aulab.cl',
        address='Asturias 220',
        phone='948369755',
        logo='logo_aulab',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_institutions),
    ]
