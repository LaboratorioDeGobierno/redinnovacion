# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0020_institution_kind'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institution',
            name='kind',
        ),
        migrations.AddField(
            model_name='institution',
            name='kind',
            field=models.IntegerField(default=1, verbose_name='kind', choices=[(1, b'Ministerio'), (2, b'Servicios'), (3, 'Empresas p\xfablicas'), (4, b'Universidades')]),
        ),
    ]
