# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0023_documentationfile_hash_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicationKind',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('name', models.CharField(default=b'Publicaci\xc3\xb3n', unique=True, max_length=100, verbose_name='name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='publication',
            name='short_description',
            field=models.CharField(default=b'', max_length=50, verbose_name='short description'),
        ),
        migrations.AddField(
            model_name='publication',
            name='kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='documentation.PublicationKind', null=True),
        ),
    ]
