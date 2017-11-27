# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_documents(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    File = apps.get_model('documents', 'File')
    Photo = apps.get_model('documents', 'Photo')

    File.objects.create(
        title='Paper de innovación',
        archive='paper_innovacion',
        description='Caso de estudio sobre los nuevos avances innovadores',
    )

    File.objects.create(
        title='Paper toma de decisiones',
        archive='paper_toma_decisiones',
        description='Caso de estudio toma de decisiones en las empresas',
    )
    Photo.objects.create(
        title='Primera charla de innovación',
        photo='banner_innovacion',
    )

    Photo.objects.create(
        title='Primera charla toma de decisiones',
        photo='banner_toma_decisiones',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_documents),
    ]
