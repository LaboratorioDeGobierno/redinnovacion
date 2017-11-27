# -*- coding: utf-8 -*-
""" Administration classes for the dynamic_contents application. """
# standard library

# django
from django.contrib import admin

# models
from .models import DynamicContent


@admin.register(DynamicContent)
class DynamicContentAdmin(admin.ModelAdmin):
    pass
