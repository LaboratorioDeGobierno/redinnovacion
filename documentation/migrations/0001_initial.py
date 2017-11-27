# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base.models
import documentation.enums


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Documentation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('title', models.CharField(default=b'', max_length=255, verbose_name='title')),
                ('archive', models.FileField(upload_to=base.models.file_path, verbose_name='archive')),
                ('description', models.TextField(default=b'', verbose_name='description')),
                ('kind', models.PositiveSmallIntegerField(default=0, verbose_name='kind', choices=[(0, 'Tool'), (1, 'Methodology')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, documentation.enums.DocumentationEnum),
        ),
    ]
