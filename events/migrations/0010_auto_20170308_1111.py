# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_events(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Event = apps.get_model('events', 'Event')
    Activity = apps.get_model('activities', 'Activity')

    event_1 = Event(
        name="Evento de prueba 1",
        description="Descripcion de evento de prueba 1",
        address="Asturias 220",
    )
    event_1.save()
    event_2 = Event(
        name="Evento de prueba 2",
        description="Descripcion de evento de prueba 2",
        address="Asturias 020",
    )
    event_2.save()

    Activity.objects.create(
        name="Actividad de prueba para evento 1",
        description="Descripcion de actividad de prueba para evento 1",
        event=event_1
    )
    Activity.objects.create(
        name="Actividad de prueba para evento 2",
        description="Descripcion de actividad de prueba para evento 2",
        event=event_2
    )


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20170308_1110'),
        ('activities', '0002_auto_20170308_1109'),
    ]

    operations = [
        migrations.RunPython(create_events),
    ]
