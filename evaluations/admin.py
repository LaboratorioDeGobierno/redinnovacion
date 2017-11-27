from django.contrib import admin

from evaluations.models import EventEvaluation


class EventEvaluationAdmin(admin.ModelAdmin):
    list_display = ('event', 'activity', 'user')


admin.site.register(EventEvaluation, EventEvaluationAdmin)
