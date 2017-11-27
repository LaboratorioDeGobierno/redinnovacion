# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_auto_20170103_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='description',
            field=models.TextField(default=b'', verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='file',
            name='title',
            field=models.CharField(default=b'', max_length=255, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='title',
            field=models.CharField(default=b'', max_length=255, verbose_name='title'),
        ),
    ]
