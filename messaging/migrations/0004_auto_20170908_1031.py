# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0003_auto_20170906_2039'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailmessage',
            options={'ordering': ('-id',)},
        ),
    ]
