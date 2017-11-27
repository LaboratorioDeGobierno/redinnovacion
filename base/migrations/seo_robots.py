# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def add_rules(apps, schema_editor):
    # models
    Site = apps.get_model('sites', 'Site')
    Url = apps.get_model('robots', 'Url')
    Rule = apps.get_model('robots', 'Rule')
    # get site
    site = Site.objects.first()
    # create urls
    url, created = Url.objects.get_or_create(
        pattern='/admin'
    )
    # create rules
    rule, created = Rule.objects.get_or_create(
        robot="*"
    )
    if site:
        rule.sites.add(site)

    rule.disallowed.add(url)


class Migration(migrations.Migration):

    dependencies = [
        ('robots', '0001_initial'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_rules)
    ]
