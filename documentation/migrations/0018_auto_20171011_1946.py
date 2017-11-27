# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documentation', '0017_documentationsearch'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentationSearchLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='documentationsearch',
            name='user',
        ),
        migrations.AlterField(
            model_name='documentationsearch',
            name='search',
            field=models.CharField(unique=True, max_length=255, verbose_name='search'),
        ),
        migrations.AlterField(
            model_name='documentationsearch',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, null=True, verbose_name='slug'),
        ),
        migrations.AddField(
            model_name='documentationsearchlog',
            name='documentation_search',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='documentation search', blank=True, to='documentation.DocumentationSearch', null=True),
        ),
        migrations.AddField(
            model_name='documentationsearchlog',
            name='user',
            field=models.ForeignKey(related_name='documentation_searched', verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
