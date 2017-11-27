# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documentation', '0016_tool_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentationSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('search', models.CharField(max_length=255, verbose_name='search')),
                ('slug', models.SlugField(max_length=100, null=True, verbose_name='slug')),
                ('user', models.ForeignKey(related_name='documentation_searched', on_delete=django.db.models.deletion.SET_NULL, verbose_name='user', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
