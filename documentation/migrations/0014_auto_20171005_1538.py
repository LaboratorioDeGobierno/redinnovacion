# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0013_auto_20171004_1902'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentationTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='name file')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='methodology',
            name='tags',
            field=models.ManyToManyField(to='documentation.DocumentationTag', verbose_name='tags', blank=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='tags',
            field=models.ManyToManyField(to='documentation.DocumentationTag', verbose_name='tags', blank=True),
        ),
        migrations.AddField(
            model_name='tool',
            name='tags',
            field=models.ManyToManyField(to='documentation.DocumentationTag', verbose_name='tags', blank=True),
        ),
    ]
