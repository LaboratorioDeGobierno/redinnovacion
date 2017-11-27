# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('description', models.CharField(max_length=1500, verbose_name='description')),
                ('start_date', models.DateTimeField(verbose_name='start date')),
                ('end_date', models.DateTimeField(null=True, verbose_name='final date')),
                ('address', models.CharField(max_length=50, verbose_name='address')),
                ('quota', models.IntegerField(verbose_name='quota')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('event', models.ForeignKey(related_name='events', on_delete=django.db.models.deletion.SET_NULL, verbose_name='event', to='events.Event', null=True)),
                ('manager', models.ForeignKey(related_name='activities_activity_manager', verbose_name='manager', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
