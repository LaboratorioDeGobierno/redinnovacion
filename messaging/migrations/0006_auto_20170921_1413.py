# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0005_emailnotification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailnotification',
            name='email_message',
        ),
        migrations.RemoveField(
            model_name='emailnotification',
            name='notification',
        ),
        migrations.DeleteModel(
            name='EmailNotification',
        ),
    ]
