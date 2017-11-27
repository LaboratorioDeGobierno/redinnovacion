# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0019_documentationsearch_highlighted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='author',
            field=models.CharField(default=b'', max_length=255, verbose_name='author'),
        ),
    ]
