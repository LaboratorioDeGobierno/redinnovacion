# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0007_auto_20170208_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, verbose_name='phone'),
        ),
    ]
