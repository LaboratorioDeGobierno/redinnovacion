# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from documents.models import File, Photo


def create_cases(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Case = apps.get_model('cases', 'Case')
    File = apps.get_model('documents', 'File')

    file_case = File.objects.create(
        title='Paper de tecnologias que ayudan a innovar',
        archive='paper_tecnologias',
        description='Caso de estudio sobre tecnologias que ayudan a innovar',
    )
    Case.objects.create(
        title='Paper de innovacion en aulab',
        publication_date='2016-12-09',
        archive=file_case
    )

    Case.objects.create(
        title='Paper de toma de desiciones en el nuevo mercado',
        publication_date='2016-12-09',
        archive=file_case
    )


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0002_auto_20170103_1653'),
    ]

    operations = [
        migrations.RunPython(create_cases),
    ]
