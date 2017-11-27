# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documentation', '0003_auto_20170929_1539'),
    ]

    operations = [
        migrations.CreateModel(
            name='Methodology',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('title', models.CharField(default=b'', max_length=255, verbose_name='title')),
                ('about', models.TextField(default=b'', verbose_name='about')),
                ('description', models.TextField(default=b'', verbose_name='description')),
                ('download_file', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='download file', blank=True, to='documentation.DownloadFile', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('title', models.CharField(default=b'', max_length=255, verbose_name='title')),
                ('about', models.TextField(default=b'', verbose_name='about')),
                ('description', models.TextField(default=b'', verbose_name='description')),
                ('author', models.ForeignKey(related_name='publications', verbose_name='author', to=settings.AUTH_USER_MODEL)),
                ('download_file', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='download file', blank=True, to='documentation.DownloadFile', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
