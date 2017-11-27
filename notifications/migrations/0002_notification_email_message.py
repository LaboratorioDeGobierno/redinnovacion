# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0006_auto_20170921_1413'),
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='email_message',
            field=models.OneToOneField(null=True, blank=True, to='messaging.EmailMessage', verbose_name='email message'),
        ),
    ]
