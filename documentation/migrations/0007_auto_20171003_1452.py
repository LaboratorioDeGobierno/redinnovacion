# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0006_auto_20171003_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='methodology',
            name='download_file',
            field=models.ForeignKey(verbose_name='download file', blank=True, to='documentation.DownloadFile', null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='download_file',
            field=models.ForeignKey(verbose_name='download file', blank=True, to='documentation.DownloadFile', null=True),
        ),
        migrations.AlterField(
            model_name='tool',
            name='download_file',
            field=models.ForeignKey(verbose_name='download file', blank=True, to='documentation.DownloadFile', null=True),
        ),
    ]
