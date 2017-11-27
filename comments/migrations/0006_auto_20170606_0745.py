# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0005_auto_20170605_1035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentimage',
            name='comment',
        ),
        migrations.AddField(
            model_name='comment',
            name='images',
            field=models.ManyToManyField(to='comments.CommentImage', verbose_name='images', blank=True),
        ),
    ]
