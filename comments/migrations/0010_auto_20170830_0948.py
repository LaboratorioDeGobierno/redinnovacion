# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0009_comment_user_mentions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commentlike',
            options={'ordering': ('-id',)},
        ),
    ]
