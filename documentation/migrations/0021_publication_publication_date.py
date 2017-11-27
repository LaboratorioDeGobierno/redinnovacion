# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0020_auto_20171017_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='publication_date',
            field=models.DateField(default=datetime.datetime(2017, 10, 18, 15, 28, 39, 524215, tzinfo=utc), verbose_name='publication date'),
            preserve_default=False,
        ),
    ]
