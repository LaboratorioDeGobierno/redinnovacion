# django
from django.contrib import admin

# import export
from import_export.admin import ImportExportModelAdmin

# models
from regions.models import Region, County


class RegionAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'short_name')


admin.site.register(Region, RegionAdmin)
admin.site.register(County)
