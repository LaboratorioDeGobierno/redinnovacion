# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def create_institutions_kinds(apps, schema_editor):
    # import institution kind model
    InstitutionKind = apps.get_model('institutions', 'InstitutionKind')

    # create institution kinds
    InstitutionKind.objects.create(pk=1, name='Ministerio')
    InstitutionKind.objects.create(pk=2, name='Servicios')
    InstitutionKind.objects.create(pk=3, name=u'Empresas públicas')
    InstitutionKind.objects.create(pk=4, name='Universidades')
    InstitutionKind.objects.create(pk=5, name='Otro')


def delete_all(apps, schema_editor):
    # import institution kind model
    InstitutionKind = apps.get_model('institutions', 'InstitutionKind')

    # delete all rows
    InstitutionKind.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0021_auto_20170921_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstitutionKind',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='creation date', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='edition date', auto_now=True, null=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(create_institutions_kinds, delete_all),
        migrations.AlterField(
            model_name='institution',
            name='kind',
            field=models.ForeignKey(related_name='institutions', on_delete=django.db.models.deletion.SET_NULL, verbose_name='institution kind', to='institutions.InstitutionKind', null=True),
        ),
    ]
