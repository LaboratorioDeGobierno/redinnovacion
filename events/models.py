# -*- coding: utf-8 -*-
# django
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Avg
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from regions.models import Region
from regions.models import County
from base.models import BaseModel, file_path
from users.models import User

from easy_thumbnails.fields import ThumbnailerImageField

from .managers import EventQueryset
from .managers import StageQuerySet

from base import utils

# faker
from faker import Faker

# random
from random import randint


class Event(BaseModel):
    class ACTIVITY_TYPES(object):
        WORKSHOP = 'Workshop'
        MEETING = 'Meeting'
        TALK = 'Talk'
        EVENT = 'Event'
        EXTERNAL = 'Others'
        EXPERIMENTA = 'Experimenta'

        choices = (
            (WORKSHOP, _('Workshop')),
            (MEETING, _('Meeting')),
            (TALK, _('Talk')),
            (EVENT, _('Event')),
            (EXTERNAL, _('Others')),
            (EXPERIMENTA, 'Experimenta'),
        )

        colors = {
            WORKSHOP: 'Workshop',
            MEETING: 'Meeting',
            TALK: 'Talk',
            EVENT: 'Event',
            EXTERNAL: 'others',
        }

    class Meta:
        ordering = ('-highlighted', 'start_date')

    # foreign keys
    region = models.ForeignKey(
        Region,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('region'),
    )
    county = models.ForeignKey(
        County,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('county'),
    )
    experts = models.ManyToManyField(
        'users.User',
        verbose_name=_('experts'),
        related_name='%(app_label)s_%(class)s_experts',
        blank=True,
    )
    creator = models.ForeignKey(
        'users.User',
        verbose_name=_('creator'),
        related_name='created_events',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    manager = models.ForeignKey(
        'users.User',
        verbose_name=_('manager'),
        related_name='%(app_label)s_%(class)s_manager',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    participants = models.ManyToManyField(
        'users.User',
        verbose_name=_('participants'),
        related_name='%(app_label)s_%(class)s_participants',
        blank=True,
    )
    institutions = models.ManyToManyField(
        'institutions.Institution',
        verbose_name=_('institutions'),
        related_name='%(app_label)s_%(class)s_institutions',
        blank=True,
    )
    files = models.ManyToManyField(
        'documents.File',
        verbose_name=_('files'),
        related_name='%(app_label)s_%(class)s_files',
        blank=True,
    )
    photos = models.ManyToManyField(
        'documents.Photo',
        verbose_name=_('photos'),
        related_name='%(app_label)s_%(class)s_photos',
        blank=True,
    )
    # required fields
    name = models.CharField(
        _('name'),
        max_length=100,
    )
    description = models.TextField(
        _('description'),
    )
    what_does_it_consist_of = models.TextField(
        u'¿En qué consiste el taller/tipo de actividad?',
        default='',
    )
    tags = models.CharField(
        _('tags'),
        default='',
        max_length=255,
    )
    presentation = models.FileField(
        null=True,
        blank=True,
        upload_to=file_path,
    )
    address = models.CharField(
        _('address'),
        max_length=255,
    )
    place = models.CharField(
        _('place'),
        max_length=255,
        default='',
    )
    # optional fields
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
    principal_image = ThumbnailerImageField(
        _('principal image'),
        upload_to=file_path,
        null=True,
        blank=True,
    )
    activity_type = models.CharField(
        _('type of activity'),
        max_length=50,
        choices=ACTIVITY_TYPES.choices,
        default=ACTIVITY_TYPES.choices[0][0],
    )
    contact_email = models.EmailField(
        _('contact email'),
        null=True,
        blank=True,
    )
    url = models.URLField(
        _('url'),
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        _('is active'),
        default=True,
    )
    acreditation = models.BooleanField(
        _('acreditation'),
        default=False,
    )
    quota = models.IntegerField(
        _('quota'),
        null=True,
        blank=True,
    )
    google_maps_iframe = models.TextField(
        _('google maps iframe'),
        default='',
        blank=True,
    )
    highlighted = models.BooleanField(
        _('highlighted'),
        default=False,
    )
    certification_text = models.TextField(
        _('certification text'),
        default='',
        blank=True,
    )
    objects = EventQueryset.as_manager()

    @classmethod
    def get_events_for_calendar(cls, user, start_date, end_date, **kwargs):
        """
        Get events for the calendar by date range
        """
        events = cls.objects.between_dates(
            start_date,
            end_date,
        ).filter(is_active=True)

        if not user.is_experimenta() and not user.is_staff:
            events = events.exclude(
                activity_type=Event.ACTIVITY_TYPES.EXPERIMENTA
            )

        if 'region_id' in kwargs and kwargs['region_id']:
            events = events.filter(region_id=kwargs['region_id'])

        if 'hide_events' in kwargs and kwargs['hide_events']:
            events = events.exclude(activity_type=cls.ACTIVITY_TYPES.EVENT)

        if 'hide_workshops' in kwargs and kwargs['hide_workshops']:
            events = events.exclude(activity_type=cls.ACTIVITY_TYPES.WORKSHOP)

        if 'hide_meetings' in kwargs and kwargs['hide_meetings']:
            events = events.exclude(activity_type=cls.ACTIVITY_TYPES.MEETING)

        if 'hide_talks' in kwargs and kwargs['hide_talks']:
            events = events.exclude(activity_type=cls.ACTIVITY_TYPES.TALK)

        if 'hide_experimenta' in kwargs and kwargs['hide_experimenta']:
            events = events.exclude(
                activity_type=cls.ACTIVITY_TYPES.EXPERIMENTA
            )

        res = []
        for event in events:
            if event.is_activity_active():
                event_dict = {}
                event_dict['title'] = event.name
                event_dict['start'] = timezone.localtime(event.start_date)
                event_dict['end'] = timezone.localtime(event.end_date)
                event_dict['type'] = event.activity_type.lower()
                event_dict['eventUrl'] = event.get_absolute_url()
                event_dict['startStr'] = timezone.localtime(
                    event.start_date).time().strftime('%H:%M')
                event_dict['endStr'] = timezone.localtime(
                    event.end_date).time().strftime('%H:%M')

                if event.region:
                    event_dict['region'] = event.region.name
                else:
                    event_dict['region'] = ''

                if event.county:
                    event_dict['county'] = event.county.name
                else:
                    event_dict['county'] = ''

                if not event.is_over():
                    stage = event.stage_set.active().get_current_stage()
                    if stage:
                        if stage.stage_type == stage.STAGE_TYPE_INSCRIPTION:
                            activity = event.get_base_activity()
                            event_dict['registerUrl'] = reverse(
                                'user_activity_create',
                                kwargs={'pk': activity.id},
                            )

                res.append(event_dict)
        return res

    def __unicode__(self):
        return self.name

    # django methods
    def get_absolute_url(self):
        return str(reverse(
            'event_detail', kwargs={
                'pk': self.pk
            }
        ))

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip()

        return super(Event, self).save(*args, **kwargs)

    # public methods
    def get_evaluation_average(self):
        return self.eventevaluation_set.all().aggregate(
            Avg('satisfaction')
        )['satisfaction__avg']

    def get_invitation_link(self, user, use_https=False):
        if not user.token:
            user.set_token()

        protocol = use_https and 'https' or 'http'

        path = reverse(
            'event_detail_with_login', kwargs={
                'pk': self.pk,
                'token': user.token,
                'email': user.email,
            }
        )

        domain = Site.objects.get_current().domain

        return '{}://{}{}'.format(protocol, domain, path)

    def get_activities_list_html(self, user):
        from activities.models import UserActivity

        # TODO: do this in a single query for Activities
        user_activities = UserActivity.objects.filter(
            activity__event=self,
            user=user,
        ).select_related('activity')

        activities = []
        for user_activity in user_activities:
            activity = user_activity.activity
            activities.append(activity)

        html = render_to_string(
            'emails/includes/activities_list.jade',
            context={
                'activities': activities,
            },
        ).replace('\n  ', '').replace('\n', '')
        return html

    def get_base_activity(self):
        if not self.activity_set.exists():
            self.activity_set.create(
                event=self,
                name=self.name,
                region_id=self.region_id,
                start_date=self.start_date,
                quota=self.quota,
            )
        return self.activity_set.first()

    def get_base_comments(self):
        comments = self.comment_set.base_comments()
        return comments.prefetch_related('comment_set', 'images')

    def get_stages(self):
        return self.stage_set.filter(is_active=True)

    def get_tags(self):
        return (tag.strip() for tag in self.tags.split(','))

    def is_over(self):
        if self.end_date:
            return self.end_date.date() < utils.today()
        return False

    def is_activity_active(self):
        stages = self.stage_set.all()
        activity = stages.filter(stage_type=Stage.STAGE_TYPE_ACTIVITY)
        # must be unique
        if activity.exists():
            return activity.first().is_active
        else:
            return True

    def is_experimenta(self):
        """
        Check if this event is an experimenta event
        """
        return self.activity_type == Event.ACTIVITY_TYPES.EXPERIMENTA

    @classmethod
    def add_user_to_experimenta_events(cls, user):
        """
        Add user to experimenta events
        """
        experimenta_events = cls.objects.filter(
            activity_type=cls.ACTIVITY_TYPES.EXPERIMENTA
        )

        for experimenta_event in experimenta_events:
            activity = experimenta_event.get_base_activity()
            activity.register_assistant(user)

    def add_experimenta_users(self):
        """
        Add experimenta users to this event
        """
        experimenta_users = User.experimenta_users()
        activity = self.get_base_activity()
        for user in experimenta_users:
            activity.register_assistant(user)

    @classmethod
    def generate(cls, quantity):
        fake = Faker()
        events = []
        for i in range(quantity):
            activity_type = Event.ACTIVITY_TYPES.choices[randint(0, 5)]
            event = {
                'name': fake.sentence(
                    nb_words=4, variable_nb_words=True, ext_word_list=None
                ),
                'description': fake.text(),
                'activity_type': activity_type[0],
                'get_activity_type_display': activity_type[1],
                'start_date': fake.date_time_this_month(),
            }
            events.append(event)

        return events

    @classmethod
    def get_dict_event_colors(cls):
        res = {}
        res[cls.ACTIVITY_TYPES.WORKSHOP] = '#F6A623'
        res[cls.ACTIVITY_TYPES.MEETING] = '#007AFF'
        res[cls.ACTIVITY_TYPES.TALK] = '#5856D6'
        res[cls.ACTIVITY_TYPES.EVENT] = '#FF2D55'
        res[cls.ACTIVITY_TYPES.EXTERNAL] = '#5AC8FA'
        res[cls.ACTIVITY_TYPES.EXPERIMENTA] = '#BBFFCC'
        return res


class Stage(BaseModel):
    STAGE_TYPE_INSCRIPTION = 2
    STAGE_TYPE_ACTIVITY = 4
    STAGE_TYPE_EVALUATION = 5
    STAGE_TYPES = (
        (1, u"Convocatoria"),
        (STAGE_TYPE_INSCRIPTION, u"Inscripcion"),
        (3, u"Acreditación"),
        (STAGE_TYPE_ACTIVITY, u"Actividad"),
        (STAGE_TYPE_EVALUATION, u"Evaluación")
    )
    name = models.CharField(
        _('name'),
        max_length=50,
        null=True,
        blank=True,
    )
    description = models.TextField(
        _('description'),
        null=True,
        blank=True,
    )
    start_date = models.DateTimeField(
        _('start date'),
        null=True,
    )
    end_date = models.DateTimeField(
        _('final date'),
        null=True,
    )
    stage_type = models.PositiveSmallIntegerField(
        verbose_name=_("Type Stage"),
        choices=STAGE_TYPES,
        null=True,
        blank=True,
    )
    event = models.ForeignKey(
        'Event',
        verbose_name=_('event'),
    )
    is_active = models.BooleanField(
        _('is active'),
        default=True,
    )

    objects = StageQuerySet.as_manager()

    class Meta:
        ordering = ('start_date',)

    def __unicode__(self):
        return self.name or u''

    def clean(self, *args, **kwargs):
        if self.start_date is None or self.end_date is None:
            return

        if self.start_date >= self.end_date:
            inverted_msg = _('End date must be after start date')
            raise ValidationError({'end_date': inverted_msg})

    def get_absolute_url(self):
        return reverse('stage_detail', kwargs={'pk': self.pk})

    def is_current_stage(self):
        if not self.start_date:
            return False
        now = timezone.now()
        if self.start_date > now:
            return False
        if not self.end_date:
            return True
        return self.end_date >= now

    def has_started(self):
        if not self.start_date:
            return False
        now = timezone.now()
        return self.start_date <= now

    def has_finished(self):
        if not self.end_date:
            return False
        now = timezone.now()
        return self.end_date < now

    def progress_percentage(self):
        now = timezone.now()

        if not self.start_date or now <= self.start_date:
            return 0
        if not self.end_date or now >= self.end_date:
            return 100

        total_days = (self.end_date - self.start_date).days
        progress_days = (now - self.start_date).days

        if total_days:
            return (progress_days * 100) / total_days

        return 0


class UserEvent(BaseModel):
    user = models.ForeignKey(
        'users.User',
        verbose_name=_('user'),
    )
    event = models.ForeignKey(
        Event,
        verbose_name=_('event'),
    )
    attendance_date = models.DateTimeField(
        verbose_name=_('attendance date'),
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return self.user.email


@receiver(m2m_changed, sender=User.groups.through,
          dispatch_uid="add_experimenta_events")
def add_experimenta_users_to_events(sender, instance, **kwargs):
    """
    Add experimenta user (created or edited) to experimenta events
    """
    if instance.is_experimenta():
        Event.add_user_to_experimenta_events(instance)


@receiver(post_save, sender=Event)
def event_post_save(sender, instance, created, **kwargs):
    if created:
        from notifications.models import Notification

        notifications = []

        notification_kwargs = {
            'event': instance,
            'kind': Notification.EVENT,
        }

        user_ids = User.objects.all().members().values_list('id', flat=True)
        for user_id in user_ids:
            notification_kwargs['user_id'] = user_id
            notifications.append(
                Notification(**notification_kwargs)
            )

        Notification.objects.bulk_create(notifications)
