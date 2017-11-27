# -*- coding: utf-8 -*-
""" Administration classes for the documentation application. """
# standard library

# django
from django.contrib import admin
from django.db.models import Count

# models
from .models import DocumentationSearch
from .models import Methodology
from .models import Publication
from .models import PublicationKind
from .models import Tool


class MethodologyAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title',
    )
    search_fields = ['title']


admin.site.register(Methodology, MethodologyAdmin)


class ToolAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title',
    )
    search_fields = ['title']


admin.site.register(Tool, ToolAdmin)


class PublicationKindAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


admin.site.register(PublicationKind, PublicationKindAdmin)


class PublicationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'highlighted'
    )
    search_fields = ['title']


admin.site.register(Publication, PublicationAdmin)


class DocumentationSearchAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'search', 'highlighted', 'search_count',
    )
    ordering = ('-documentationsearchlog__count', '-highlighted',)

    def get_queryset(self, request):
        qs = super(DocumentationSearchAdmin, self).get_queryset(request)
        qs = qs.annotate(Count('documentationsearchlog'))
        return qs

    def search_count(self, obj):
        return obj.documentationsearchlog__count
    search_count.admin_order_field = 'documentationsearchlog__count'


admin.site.register(DocumentationSearch, DocumentationSearchAdmin)
