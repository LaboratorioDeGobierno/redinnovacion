# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import dynamic_contents.enums


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_auto_20170711_1525'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documentation', '0021_publication_publication_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('name', models.CharField(max_length=30, verbose_name='name', blank=True)),
                ('value', models.TextField(verbose_name='value', blank=True)),
                ('kind', models.CharField(default=b'html', max_length=30, verbose_name='kind', blank=True, choices=[(b'gallery', 'gallery'), (b'html', 'HTML'), (b'video', 'Video')])),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_by', models.ForeignKey(verbose_name='created by', to=settings.AUTH_USER_MODEL)),
                ('methodology', models.ForeignKey(blank=True, to='documentation.Methodology', null=True)),
                ('photos', models.ManyToManyField(to='documents.Photo', blank=True)),
                ('tool', models.ForeignKey(blank=True, to='documentation.Tool', null=True)),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'dynamic content',
                'verbose_name_plural': 'dynamic contents',
                'permissions': (('view_dynamiccontent', 'Can view dynamic content'),),
            },
            bases=(models.Model, dynamic_contents.enums.DynamicContentKinds),
        ),
    ]
