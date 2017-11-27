# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cases', '0007_auto_20171020_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='editor',
            field=models.ForeignKey(related_name='edited_cases', on_delete=django.db.models.deletion.SET_NULL, verbose_name='editor', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
