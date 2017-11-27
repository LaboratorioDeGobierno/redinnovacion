# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0021_publication_publication_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='publication_date',
            field=models.DateField(null=True, verbose_name='publication date', blank=True),
        ),
    ]
