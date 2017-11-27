# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('interest', models.CharField(max_length=50, verbose_name='interest')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='order')),
            ],
            options={
                'ordering': ('order', 'interest'),
            },
        ),
    ]
