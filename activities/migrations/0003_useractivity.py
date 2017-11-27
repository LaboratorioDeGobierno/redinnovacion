# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0010_auto_20170308_1111'),
        ('activities', '0002_auto_20170308_1109'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('attendance_date', models.DateTimeField(null=True, verbose_name='attendance date', blank=True)),
                ('activity', models.ForeignKey(verbose_name='user', to='activities.Activity')),
                ('stage', models.ForeignKey(verbose_name='user', blank=True, to='events.Stage', null=True)),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
