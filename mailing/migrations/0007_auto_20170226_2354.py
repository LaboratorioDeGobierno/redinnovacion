# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0006_auto_20170226_0452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='html_body',
            field=models.TextField(),
        ),
    ]
