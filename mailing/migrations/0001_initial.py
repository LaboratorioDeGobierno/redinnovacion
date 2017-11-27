# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mailing.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('subject', models.CharField(max_length=255)),
                ('text_header', models.TextField()),
                ('html_header', models.TextField()),
                ('text_body', models.TextField()),
                ('html_body', models.TextField()),
                ('text_footer', models.TextField()),
                ('html_footer', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MailImages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('image', models.ImageField(upload_to=mailing.models.image_file_path)),
                ('mail', models.ForeignKey(related_name='images', to='mailing.Mail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MailTarget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('attribute_name', models.CharField(max_length=255)),
                ('attribute_value', models.CharField(max_length=255)),
                ('mail', models.ForeignKey(related_name='targets', to='mailing.Mail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MailTargetStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('status', models.IntegerField(default=0, verbose_name='status', choices=[(0, 'Not Sent'), (1, 'Sent'), (2, 'Error'), (3, 'Other')])),
                ('sent_at', models.DateTimeField(null=True, verbose_name='sent at', blank=True)),
                ('target', models.ForeignKey(related_name='target_statuses', to='mailing.MailTarget')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
