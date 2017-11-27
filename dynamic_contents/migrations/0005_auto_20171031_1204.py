# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_contents', '0004_dynamiccontent_case'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamiccontent',
            name='kind',
            field=models.CharField(default=b'html', max_length=30, verbose_name='kind', blank=True, choices=[(b'gallery', 'gallery'), (b'image', 'image'), (b'html', 'HTML'), (b'video', 'Video')]),
        ),
    ]
