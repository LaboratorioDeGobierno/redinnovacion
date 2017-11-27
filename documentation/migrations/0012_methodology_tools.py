# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0011_publication_highlighted'),
    ]

    operations = [
        migrations.AddField(
            model_name='methodology',
            name='tools',
            field=models.ManyToManyField(to='documentation.Tool', verbose_name='tools', blank=True),
        ),
    ]
