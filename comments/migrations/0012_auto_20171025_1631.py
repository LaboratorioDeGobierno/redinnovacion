# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0023_documentationfile_hash_id'),
        ('comments', '0011_comment_highlighted'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='methodology',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='documentation.Methodology', null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='tool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='documentation.Tool', null=True),
        ),
    ]
