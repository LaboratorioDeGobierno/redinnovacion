# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0041_auto_20170601_0921'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('subject', models.CharField(max_length=78, verbose_name='subject', blank=True)),
                ('body', models.TextField(verbose_name='body', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='institution',
            field=models.ForeignKey(related_name='users', on_delete=django.db.models.deletion.SET_NULL, verbose_name='institution', to='institutions.Institution', null=True),
        ),
        migrations.AddField(
            model_name='usermessage',
            name='receiver',
            field=models.ForeignKey(related_name='receivermessage_set', verbose_name='sender', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='usermessage',
            name='sender',
            field=models.ForeignKey(related_name='sendermessage_set', verbose_name='sender', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
