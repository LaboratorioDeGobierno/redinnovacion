# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0008_auto_20170713_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user_mentions',
            field=models.ManyToManyField(related_name='comment_mentions', verbose_name='user mentions', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
