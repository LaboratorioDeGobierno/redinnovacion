# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20170109_1205'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('show_name', models.BooleanField(default=True, verbose_name='show name')),
                ('show_charge', models.BooleanField(default=True, verbose_name='show charge')),
                ('show_institution', models.BooleanField(default=True, verbose_name='show institution')),
                ('show_email', models.BooleanField(default=True, verbose_name='show email')),
                ('show_phone', models.BooleanField(default=True, verbose_name='show phone')),
                ('show_interests', models.BooleanField(default=True, verbose_name='show interests')),
                ('description', models.TextField(verbose_name='description')),
                ('user', models.OneToOneField(related_name='user_profile', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
