# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0042_auto_20170612_2213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermessage',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='usermessage',
            name='sender',
        ),
        migrations.DeleteModel(
            name='UserMessage',
        ),
    ]
