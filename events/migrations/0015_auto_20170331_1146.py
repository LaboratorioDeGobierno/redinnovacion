# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_auto_20170320_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='contact_email',
            field=models.EmailField(max_length=254, null=True, verbose_name='contact email', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='url',
            field=models.URLField(null=True, verbose_name='url', blank=True),
        ),
    ]
