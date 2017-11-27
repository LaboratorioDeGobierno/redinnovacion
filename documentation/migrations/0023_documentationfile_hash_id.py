# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0022_auto_20171023_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentationfile',
            name='hash_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
