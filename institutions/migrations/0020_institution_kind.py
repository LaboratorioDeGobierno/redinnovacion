# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0019_institution_role_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='kind',
            field=models.CharField(default=1, max_length=255, verbose_name='kind', choices=[(1, b'Ministerio'), (2, b'Servicios'), (3, 'Empresas p\xfablicas'), (4, b'Universidades')]),
        ),
    ]
