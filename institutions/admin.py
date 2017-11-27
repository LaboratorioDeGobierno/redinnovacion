from django.contrib import admin
from .models import Institution

# import export
from import_export.admin import ImportExportModelAdmin


class InstitutionAdmin(ImportExportModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    import_id_fields = ('name', 'role_description')
    export_order = ('name', 'role_description')


admin.site.register(Institution, InstitutionAdmin)
