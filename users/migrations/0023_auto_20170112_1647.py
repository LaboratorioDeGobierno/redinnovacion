# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20170112_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='topic_of_interest',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='topic_of_interests',
            field=models.ManyToManyField(related_name='user_profile', verbose_name='topic of interests', to='users.TopicOfInterest'),
        ),
    ]
