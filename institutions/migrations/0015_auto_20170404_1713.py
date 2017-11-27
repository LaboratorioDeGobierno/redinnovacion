# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import itertools
from django.db import migrations, models
from django.utils.text import slugify


def populate_slug(apps, schema_editor):
    Institution = apps.get_model('institutions', 'Institution')
    institutions = Institution.objects.all()
    for institution in institutions:
        slug = slugify(institution.name)
        institution.slug = slug
        for index in itertools.count(1):
            if Institution.objects.filter(slug=institution.slug).exists():
                institution.slug = '{}-{}'.format(slug, index)
                continue
            break
        institution.save()


def blank(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0014_institution_slug'),
    ]

    operations = [
        migrations.RunPython(populate_slug, blank),
    ]
