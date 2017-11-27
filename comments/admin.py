from django.contrib import admin

from comments.models import Comment
from comments.models import CommentImage


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'activity', 'event',)


admin.site.register(Comment, CommentAdmin)


class CommentImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')


admin.site.register(CommentImage, CommentImageAdmin)
