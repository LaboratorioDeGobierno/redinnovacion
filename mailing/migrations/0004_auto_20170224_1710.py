# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0003_auto_20170213_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailChimpCampaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('external_id', models.CharField(max_length=255, null=True, blank=True)),
                ('raw_response', jsonfield.fields.JSONField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MailChimpList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('external_id', models.CharField(max_length=255, null=True, blank=True)),
                ('raw_response', jsonfield.fields.JSONField(null=True, blank=True)),
                ('mailing', models.OneToOneField(related_name='mailchimp_lists', verbose_name='mailing', to='mailing.Mailing')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='mailchimpcampaign',
            name='mailing_list',
            field=models.ForeignKey(related_name='mailchimp_list_campaigns', verbose_name='mailing list', to='mailing.MailChimpList'),
        ),
    ]
