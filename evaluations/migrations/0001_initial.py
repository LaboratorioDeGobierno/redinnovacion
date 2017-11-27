# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0009_auto_20170530_0524'),
        ('events', '0018_auto_20170530_0858'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventEvaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('satisfaction', models.IntegerField()),
                ('usefulness', models.IntegerField()),
                ('clear_topics', models.IntegerField()),
                ('comments', models.TextField(verbose_name='text')),
                ('the_best', models.TextField(verbose_name='text')),
                ('what_can_be_improved', models.TextField(verbose_name='text')),
                ('activity', models.ForeignKey(blank=True, to='activities.Activity', null=True)),
                ('event', models.ForeignKey(to='events.Event')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
