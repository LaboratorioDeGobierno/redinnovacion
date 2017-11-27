# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base.models
import datetime
import easy_thumbnails.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_auto_20170711_1525'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('regions', '0002_auto_20170530_0547'),
        ('documentation', '0019_documentationsearch_highlighted'),
        ('cases', '0006_auto_20170106_0947'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('search', models.CharField(unique=True, max_length=255, verbose_name='search')),
                ('slug', models.SlugField(max_length=100, unique=True, null=True, verbose_name='slug')),
                ('highlighted', models.BooleanField(default=False, verbose_name='highlighted')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CaseSearchLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('case_search', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='case search', blank=True, to='cases.CaseSearch', null=True)),
                ('user', models.ForeignKey(related_name='case_searched', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CaseTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='name')),
                ('slug', models.SlugField(max_length=100, unique=True, null=True, verbose_name='slug')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='case',
            name='archive',
        ),
        migrations.RemoveField(
            model_name='case',
            name='participants',
        ),
        migrations.AddField(
            model_name='case',
            name='about',
            field=models.TextField(default=b'', verbose_name='about'),
        ),
        migrations.AddField(
            model_name='case',
            name='attachments',
            field=models.ManyToManyField(to='documents.File', verbose_name='attachments', blank=True),
        ),
        migrations.AddField(
            model_name='case',
            name='author',
            field=models.ForeignKey(related_name='published_cases', on_delete=django.db.models.deletion.SET_NULL, verbose_name='author', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='case',
            name='description_logo',
            field=models.TextField(verbose_name='description logo', blank=True),
        ),
        migrations.AddField(
            model_name='case',
            name='duration',
            field=models.CharField(max_length=255, verbose_name='duration', blank=True),
        ),
        migrations.AddField(
            model_name='case',
            name='logo',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=base.models.file_path, null=True, verbose_name='logo', blank=True),
        ),
        migrations.AddField(
            model_name='case',
            name='methodologies',
            field=models.ManyToManyField(to='documentation.Methodology', verbose_name='methodologies', blank=True),
        ),
        migrations.AddField(
            model_name='case',
            name='partners',
            field=models.TextField(verbose_name='partners', blank=True),
        ),
        migrations.AddField(
            model_name='case',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='region', blank=True, to='regions.Region', null=True),
        ),
        migrations.AddField(
            model_name='case',
            name='team',
            field=models.CharField(max_length=255, verbose_name='team', blank=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='publication_date',
            field=models.DateField(default=datetime.date.today, verbose_name='publication date'),
        ),
        migrations.AlterField(
            model_name='case',
            name='title',
            field=models.CharField(default=b'', max_length=255, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='case',
            name='tags',
            field=models.ManyToManyField(to='cases.CaseTag', verbose_name='tags', blank=True),
        ),
    ]
