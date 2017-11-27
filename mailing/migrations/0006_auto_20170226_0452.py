# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0005_auto_20170224_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='html_footer',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='html_header',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='text_content',
            field=models.TextField(null=True, blank=True),
        ),
    ]
