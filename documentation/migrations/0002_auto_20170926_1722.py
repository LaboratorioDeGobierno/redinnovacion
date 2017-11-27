# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentation',
            name='kind',
            field=models.CharField(default=b'methodology', max_length=30, verbose_name='kind', choices=[(b'methodology', 'Methodology'), (b'tool', 'Tool'), (b'publication', 'Publication')]),
        ),
    ]
