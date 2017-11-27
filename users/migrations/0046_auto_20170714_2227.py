# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.text import slugify
from django.db import migrations


def forward(apps, schema_editor):
    User = apps.get_model('users', 'User')

    for self in User.objects.all():
        i = 0
        while not self.slug or User.objects.filter(slug=self.slug).exists():
            full_name = '{} {}'.format(self.first_name, self.last_name)
            self.slug = slugify(full_name)
            if not self.slug:
                email = self.email[:self.email.index('@')]
                self.slug = slugify(email)
            if i > 0:
                self.slug += '-{}'.format(i)
            i += 1
        self.save()


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0045_user_slug'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
