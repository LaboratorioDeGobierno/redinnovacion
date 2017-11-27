from django.contrib import admin
from .models import File, Photo


class FileAdmin(admin.ModelAdmin):
    list_filter = ('title', 'archive')


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title', 'photo')

admin.site.register(File, FileAdmin)
admin.site.register(Photo, PhotoAdmin)
