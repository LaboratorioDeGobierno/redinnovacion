# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mailing.models
import ckeditor_uploader.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('platforms', '0004_auto_20170210_2001'),
        ('mailing', '0002_auto_20170213_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('status', models.IntegerField(default=0, verbose_name='status', choices=[(0, 'Not Sent'), (1, 'Sent'), (2, 'Error'), (3, 'Other')])),
                ('sent_at', models.DateTimeField(null=True, verbose_name='sent at', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmailTarget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('attribute_name', models.CharField(max_length=255)),
                ('attribute_value', models.CharField(max_length=255)),
                ('platform', models.ForeignKey(related_name='email_targets', to='platforms.Platform')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('subject', models.CharField(max_length=255)),
                ('text_content', models.TextField()),
                ('html_header', ckeditor_uploader.fields.RichTextUploadingField()),
                ('html_body', ckeditor_uploader.fields.RichTextUploadingField()),
                ('html_footer', ckeditor_uploader.fields.RichTextUploadingField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('targets', models.ManyToManyField(to='mailing.EmailTarget')),
                ('template', models.ForeignKey(related_name='mailings', to='mailing.EmailTemplate')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TemplateImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('image', models.ImageField(upload_to=mailing.models.image_file_path)),
                ('template', models.ForeignKey(related_name='images', to='mailing.EmailTemplate')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='mailimages',
            name='mail',
        ),
        migrations.RemoveField(
            model_name='mailtarget',
            name='mail',
        ),
        migrations.RemoveField(
            model_name='mailtargetstatus',
            name='target',
        ),
        migrations.RemoveField(
            model_name='mailtargetstatus',
            name='user',
        ),
        migrations.DeleteModel(
            name='Mail',
        ),
        migrations.DeleteModel(
            name='MailImages',
        ),
        migrations.DeleteModel(
            name='MailTarget',
        ),
        migrations.DeleteModel(
            name='MailTargetStatus',
        ),
        migrations.AddField(
            model_name='emailstatus',
            name='mailing',
            field=models.ForeignKey(related_name='target_statuses', to='mailing.Mailing'),
        ),
        migrations.AddField(
            model_name='emailstatus',
            name='user',
            field=models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL),
        ),
    ]
