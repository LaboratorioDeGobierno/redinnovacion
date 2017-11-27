# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0009_auto_20171003_1906'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DownloadFileLog',
            new_name='DocumentationFileLog',
        ),
        migrations.RenameField(
            model_name='documentationfilelog',
            old_name='download_file',
            new_name='documentation_file',
        ),
        migrations.RemoveField(
            model_name='methodology',
            name='download_file',
        ),
        migrations.RemoveField(
            model_name='publication',
            name='download_file',
        ),
        migrations.RemoveField(
            model_name='tool',
            name='download_file',
        ),
        migrations.AddField(
            model_name='methodology',
            name='documentation_file',
            field=models.ForeignKey(verbose_name='documentation file', blank=True, to='documentation.DocumentationFile', null=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='documentation_file',
            field=models.ForeignKey(verbose_name='documentation file', blank=True, to='documentation.DocumentationFile', null=True),
        ),
        migrations.AddField(
            model_name='tool',
            name='documentation_file',
            field=models.ForeignKey(verbose_name='documentation file', blank=True, to='documentation.DocumentationFile', null=True),
        ),
    ]
