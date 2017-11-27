# -*- coding: utf-8 -*-
""" Administration classes for the notifications application. """
# standard library

# django
from django.contrib import admin

# models
from .models import Newsletter


class NewsletterAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'sent_at'
    )
    readonly_fields = ('created_at', 'updated_at', 'comments')


admin.site.register(Newsletter, NewsletterAdmin)
