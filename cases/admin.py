# -*- coding: utf-8 -*-
""" Administration classes for the documentation application. """
# standard library

# django
from django.contrib import admin
from django.db.models import Count

# models
from .models import Case
from .models import CaseSearch


class CaseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'year', 'team', 'author', 'region'
    )
    search_fields = [
        'title', 'author__first_name', 'author__last_name', 'team'
    ]


admin.site.register(Case, CaseAdmin)


class CaseSearchAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'search', 'highlighted', 'search_count',
    )
    ordering = ('-casesearchlog__count', '-highlighted',)

    def get_queryset(self, request):
        qs = super(CaseSearchAdmin, self).get_queryset(request)
        qs = qs.annotate(Count('casesearchlog'))
        return qs

    def search_count(self, obj):
        return obj.casesearchlog__count
    search_count.admin_order_field = 'casesearchlog__count'


admin.site.register(CaseSearch, CaseSearchAdmin)
