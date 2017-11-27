from django.contrib import admin
from .models import Event, Stage, UserEvent


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'activity_type', 'is_active',
                    'start_date', 'end_date', 'acreditation')
    list_filter = ('name', 'activity_type', 'institutions',
                   'experts', 'manager', 'acreditation')


class StageAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'event', 'stage_type')
    list_filter = ('name', 'description', 'start_date', 'end_date',
                   'event__name', 'stage_type')


class UserEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'attendance_date')
    list_filter = ('user', 'attendance_date')

admin.site.register(Event, EventAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(UserEvent, UserEventAdmin)
