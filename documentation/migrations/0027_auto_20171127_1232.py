# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0026_auto_20171103_1649'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='publicationkind',
            options={'verbose_name': 'publication kind', 'verbose_name_plural': 'publication kinds'},
        ),
        migrations.AlterField(
            model_name='publication',
            name='kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='kind', to='documentation.PublicationKind', null=True),
        ),
    ]
