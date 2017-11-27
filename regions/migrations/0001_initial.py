# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('name', models.CharField(help_text='The name of the county', unique=True, max_length=100, verbose_name='name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'county',
                'verbose_name_plural': 'counties',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('name', models.CharField(help_text='The name of the region', unique=True, max_length=100, verbose_name='name')),
                ('short_name', models.CharField(null=True, max_length=100, blank=True, help_text='A short name of the region', unique=True, verbose_name='short name')),
            ],
            options={
                'ordering': ('short_name', 'name'),
                'verbose_name': 'region',
                'verbose_name_plural': 'regions',
            },
        ),
        migrations.AddField(
            model_name='county',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='regions.Region', null=True),
        ),
    ]
