# -*- coding: utf-8 -*-
""" Administration classes for the notifications application. """
# standard library

# django
from django.contrib import admin

# models
from .models import EmailMessage


class EmailMessageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'from_user', 'to_user', 'subject', 'message', 'read',
    )


admin.site.register(EmailMessage, EmailMessageAdmin)
