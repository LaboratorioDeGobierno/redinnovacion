# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0032_user_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mother_family_name',
            field=models.CharField(max_length=30, null=True, verbose_name='mother family name', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='other_institution_name',
            field=models.CharField(max_length=32, null=True, verbose_name='other institution name', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='other_topics',
            field=models.CharField(max_length=140, null=True, verbose_name='other topics', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='institution',
            field=models.ForeignKey(related_name='users', on_delete=django.db.models.deletion.SET_NULL, verbose_name='institution', blank=True, to='institutions.Institution', null=True),
        ),
    ]
