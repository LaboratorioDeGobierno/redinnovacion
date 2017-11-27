# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20170111_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(related_name='profile', null=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
