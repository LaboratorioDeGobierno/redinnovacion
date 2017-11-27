# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newsletters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SentNewsletter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('sent_at', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('newsletter', models.ForeignKey(related_name='send_newsletters', verbose_name='newsletter', to='newsletters.Newsletter')),
                ('user', models.ForeignKey(related_name='newsletters', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='sentnewsletter',
            unique_together=set([('user', 'newsletter')]),
        ),
    ]
