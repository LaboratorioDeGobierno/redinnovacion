# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_notification_email_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='email_message',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='messaging.EmailMessage', verbose_name='email message'),
        ),
    ]
