# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0004_auto_20170224_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailchimpcampaign',
            name='mailing_list',
            field=models.OneToOneField(related_name='mailchimp_list_campaign', verbose_name='mailing list', to='mailing.MailChimpList'),
        ),
        migrations.AlterField(
            model_name='mailchimplist',
            name='mailing',
            field=models.OneToOneField(related_name='mailchimp_list', verbose_name='mailing', to='mailing.Mailing'),
        ),
    ]
