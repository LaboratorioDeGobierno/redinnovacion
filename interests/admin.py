from django.contrib import admin

from .models import Interest


class InterestAdmin(admin.ModelAdmin):
    list_display = ('interest', 'order',)


admin.site.register(Interest, InterestAdmin)
