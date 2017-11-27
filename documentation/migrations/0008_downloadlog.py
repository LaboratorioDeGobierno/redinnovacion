# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documentation', '0007_auto_20171003_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('download_file', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='download file', blank=True, to='documentation.DownloadFile', null=True)),
                ('user', models.ForeignKey(related_name='documentation_downloaded', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
