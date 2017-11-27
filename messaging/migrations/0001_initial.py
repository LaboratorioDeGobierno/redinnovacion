# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('subject', models.CharField(max_length=255, verbose_name='subjet')),
                ('message', models.TextField(max_length=500, verbose_name='message')),
                ('from_user', models.ForeignKey(related_name='sent_email_messages', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(related_name='received_email_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
