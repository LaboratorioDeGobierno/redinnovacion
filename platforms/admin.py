# django
from django.contrib import admin

# models
from platforms.models import Platform
from platforms.models import UserPlatformAttribute


class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Platform, PlatformAdmin)


class UserPlatformAttributeAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'name', 'value')
    search_fields = ('user__email',)

    list_filter = [
        'platform',
        'name',
        'value',
    ]


admin.site.register(UserPlatformAttribute, UserPlatformAttributeAdmin)
