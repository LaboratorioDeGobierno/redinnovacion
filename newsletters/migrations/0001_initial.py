# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import newsletters.models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0011_comment_highlighted'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('sent_at', models.DateTimeField(default=newsletters.models.get_next_estimated_newsletter_date, unique=True, verbose_name='sent at')),
                ('comments', models.ManyToManyField(to='comments.Comment', verbose_name='comments')),
            ],
            options={
                'verbose_name': 'newsletter',
                'verbose_name_plural': 'newsletters',
                'permissions': (('view_newsletter', 'Can view newsletters'),),
            },
        ),
    ]
