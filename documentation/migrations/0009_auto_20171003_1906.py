# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documentation', '0008_downloadlog'),
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadFileLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameModel(
            old_name='DownloadFile',
            new_name='DocumentationFile',
        ),
        migrations.RemoveField(
            model_name='downloadlog',
            name='download_file',
        ),
        migrations.RemoveField(
            model_name='downloadlog',
            name='user',
        ),
        migrations.DeleteModel(
            name='DownloadLog',
        ),
        migrations.AddField(
            model_name='downloadfilelog',
            name='download_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='documentation file', blank=True, to='documentation.DocumentationFile', null=True),
        ),
        migrations.AddField(
            model_name='downloadfilelog',
            name='user',
            field=models.ForeignKey(related_name='documentation_downloaded', verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
