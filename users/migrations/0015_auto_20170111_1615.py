# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20170111_1455'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicOfInterest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('topic', models.CharField(max_length=50, verbose_name='topic')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='order')),
            ],
            options={
                'ordering': ('order', 'topic'),
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='show_public_information',
            field=models.NullBooleanField(verbose_name='show public information', choices=[(False, 'No'), (True, 'Yes')]),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='time_in_ri',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='time_in_ri', choices=[(0, 'Una vez a la semana'), (1, 'Una vez cada 15 d\xedas'), (2, 'Una vez al mes'), (3, 'Solo algunas veces ocasionales al a\xf1o')]),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='topic_of_interest',
            field=models.ManyToManyField(related_name='user_profile', verbose_name='topic of interest', to='users.TopicOfInterest'),
        ),
    ]
