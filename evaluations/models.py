from django.db import models
from django.core.urlresolvers import reverse

from events.models import Event
from activities.models import Activity
from users.models import User
from base.models import BaseModel
from django.utils.translation import ugettext_lazy as _


class EventEvaluation(BaseModel):
    user = models.ForeignKey(
        User,
    )
    event = models.ForeignKey(
        Event,
    )
    activity = models.ForeignKey(
        Activity,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    satisfaction = models.IntegerField(
    )
    usefulness = models.IntegerField(
    )
    clear_topics = models.IntegerField(
    )
    comments = models.TextField(
        _('text'),
    )
    the_best = models.TextField(
        _('text'),
    )
    what_can_be_improved = models.TextField(
        _('text'),
    )

    class Meta:
        pass

    def get_absolute_url(self):
        return reverse(
            'event_evaluation_update', kwargs={
                'activity_id': self.activity_id,
                'pk': self.pk
            }
        )
