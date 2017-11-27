# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base.models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_auto_20170531_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='archive',
            field=models.FileField(upload_to=base.models.file_path, verbose_name='archive'),
        ),
    ]
