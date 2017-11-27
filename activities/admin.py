from django.contrib import admin
from .models import Activity, UserActivity

# import export
from import_export.admin import ImportExportModelAdmin


class ActivityAdmin(ImportExportModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'event', 'is_active')
    list_filter = ('name', 'start_date', 'end_date',
                   'event', 'manager')


class UserActivityAdmin(ImportExportModelAdmin):
    list_display = ('user', 'activity', 'stage', 'attendance_date')
    list_filter = ('user', 'attendance_date')


admin.site.register(Activity, ActivityAdmin)
admin.site.register(UserActivity, UserActivityAdmin)
