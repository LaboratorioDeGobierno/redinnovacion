# -*- coding: utf-8 -*-
""" Administration classes for the notifications application. """
# standard library

# django
from django.contrib import admin

# models
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'kind', 'comment', 'event', 'from_user',
        'read',
    )


admin.site.register(Notification, NotificationAdmin)
