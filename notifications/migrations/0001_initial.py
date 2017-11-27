# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import notifications.enums


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0009_comment_user_mentions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0031_auto_20170804_1542'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('url', models.CharField(max_length=255, verbose_name='url', blank=True)),
                ('kind', models.PositiveIntegerField(choices=[(1, 'MENTION'), (2, 'RESPONSE'), (3, 'REMINDER'), (4, 'MESSAGE'), (5, 'EVENT')])),
                ('text', models.CharField(max_length=255, verbose_name='text', blank=True)),
                ('read', models.BooleanField(default=False)),
                ('comment', models.ForeignKey(verbose_name='comment', blank=True, to='comments.Comment', null=True)),
                ('event', models.ForeignKey(verbose_name='event', blank=True, to='events.Event', null=True)),
                ('from_user', models.ForeignKey(related_name='created_notifications', verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'notification',
                'verbose_name_plural': 'notifications',
                'permissions': (('view_notification', 'Can view notifications'),),
            },
            bases=(models.Model, notifications.enums.NotificationKinds),
        ),
    ]
