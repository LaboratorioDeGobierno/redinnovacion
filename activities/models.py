from django.core.exceptions import MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from base.models import BaseModel
from regions.models import Region


class Activity(BaseModel):
    # foreign keys
    event = models.ForeignKey(
        'events.Event',
        verbose_name=_('event'),
    )
    region = models.ForeignKey(
        Region,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('region'),
    )
    manager = models.ForeignKey(
        'users.User',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_manager',
        verbose_name=_('manager'),
    )
    name = models.CharField(
        _('name'),
        max_length=100,
    )
    description = models.TextField(
        _('description'),
        max_length=1500,
    )
    start_date = models.DateTimeField(
        _('start date'),
        null=True,
        blank=True,
    )
    end_date = models.DateTimeField(
        _('final date'),
        null=True,
        blank=True,
    )
    address = models.CharField(
        _('address'),
        max_length=50,
        null=True,
        blank=True,
    )
    city = models.CharField(
        _('city'),
        blank=True,
        max_length=50,
        null=True,
    )
    quota = models.IntegerField(
        _('quota'),
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        _('is active'),
        default=True,
    )

    exclude_on_on_delete_test = ('event',)

    def __unicode__(self):
        return self.name

    def get_free_slots_count(self):
        if not(self.event.quota) or self.event.quota <= 0:
            return 0

        return self.event.quota - self.useractivity_set.count()

    def register_assistant(self, user):
        from events.models import Stage, UserEvent

        if self.get_free_slots_count() <= 0:
            return False, "Ya no hay cupo"  # TODO: translate

        stage, created = Stage.objects.get_or_create(
            event=self.event, stage_type=Stage.STAGE_TYPE_INSCRIPTION
        )
        UserActivity.objects.get_or_create(
            activity=self, user_id=user.id, stage=stage,
        )
        user_event, created = UserEvent.objects.get_or_create(
            event=self.event,
            user_id=user.id,
        )
        if created:
            self.quota -= 1
            self.save()
        return True, None

    def unregister_assistant(self, user):
        from events.models import Stage, UserEvent

        try:
            stage = Stage.objects.filter(
                event=self.event, stage_type=Stage.STAGE_TYPE_INSCRIPTION
            ).first()
            user_activity = UserActivity.objects.filter(
                activity=self, user_id=user.id, stage=stage,
            )
            user_event = UserEvent.objects.filter(
                event=self.event, user_id=user.id
            )
            user_activity.delete()
            user_event.delete()
        except (
            Stage.DoesNotExist or
            UserActivity.DoesNotExist or
            UserEvent or
            MultipleObjectsReturned
        ):
            return False, "Error al eliminar"

        self.quota += 1
        self.save()
        return True, None

    def deactivate(self, commit=True):
        self.is_active = False
        if commit:
            self.save()

    def get_absolute_url(self):
        return reverse('activity_detail', kwargs={'pk': self.pk})

    def users(self):
        return self.useractivity_set.all()

    def user_list(self):
        return [user_activity.user for user_activity in self.users()]

    def get_calendar_url(self):
        content = {
            'text': self.event.name,
        }

        location_params = (
            self.address, self.city, getattr(self.region, 'name', None),
        )
        location = u', '.join((unicode(x) for x in location_params if x))
        if location:
            content['location'] = location

        if self.description:
            content['details'] = self.description

        if self.start_date and self.end_date:
            content['dates'] = u'{}/{}'.format(
                self.start_date.strftime('%Y%m%dT%H%M00Z'),
                self.end_date.strftime('%Y%m%dT%H%M00Z')
            )

        return (
            u'https://www.google.com/calendar/render?action=TEMPLATE'
            u'&sf=true&output=xml&{}'
        ).format(urlencode(content))


class UserActivity(BaseModel):
    # foreign keys
    user = models.ForeignKey(
        'users.User',
        verbose_name=_('user'),
    )
    activity = models.ForeignKey(
        Activity,
        verbose_name=_('activity'),
    )
    stage = models.ForeignKey(
        'events.Stage',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('stage'),
    )
    attendance_date = models.DateTimeField(
        verbose_name=_('attendance date'),
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return self.user.email

    def attend(self, date=None):
        if date is None:
            date = timezone.now()
        self.attendance_date = date
        return self.save()


# class Workshop(ActivityBase):
#    pass


# class Meeting(ActivityBase):
#    pass


# class Talk(ActivityBase):
#    pass
