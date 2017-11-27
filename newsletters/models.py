# -*- coding: utf-8 -*-
""" Models for the newsletters application. """
# standard library
import datetime

# django
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# models
from events.models import Event
from base.models import BaseModel
from comments.models import Comment
from users.models import User

# messaging
from messaging import email_manager


def get_next_estimated_newsletter_date():
    if settings.TEST:
        return timezone.now()

    today = timezone.localtime(timezone.now()).date()

    # days up to next monday
    days_up_to_next_monday = 7 - today.weekday()

    # seven in the morning
    start_time = datetime.time(7)
    start_date = today + timezone.timedelta(days_up_to_next_monday)

    start_date_time = datetime.datetime.combine(start_date, start_time)

    tz = timezone.get_default_timezone()

    return timezone.make_aware(start_date_time, tz)


class Newsletter(BaseModel):
    # foreign keys
    comments = models.ManyToManyField(
        Comment,
        verbose_name=_('comments'),
    )
    # required fields
    # optional fields
    sent_at = models.DateTimeField(
        verbose_name=_('sent at'),
        unique=True,
        default=get_next_estimated_newsletter_date,
    )

    class Meta:
        verbose_name = _('newsletter')
        verbose_name_plural = _('newsletters')
        permissions = (
            ('view_newsletter', _('Can view newsletters')),
        )

    def __unicode__(self):
        return u'Newsletter {}'.format(self.sent_at)

    def get_absolute_url(self):
        """ Returns the canonical URL for the newsletter object """
        return reverse('newsletter_detail', args=(self.pk,))

    @classmethod
    def get_newsletter(cls, date=None):
        """
        Returns the next newsletter
        """
        # find next newsletter
        date = date if date else timezone.now()
        end = date + timezone.timedelta(days=7)
        newsletter = cls.objects.filter(
            sent_at__gte=date,
            sent_at__lte=end,
        )

        # check if exists
        if newsletter.exists():
            return newsletter.first()

        # if there is no newsletter, we create the following
        return cls.objects.create()

    @classmethod
    def get_last_newsletter(cls):
        """
        Returns the last newsletter from today
        """
        date = timezone.now() - timezone.timedelta(days=7)
        return cls.get_newsletter(date)

    def get_subject(self):
        """
        Returns the subject of the newsletter email
        """
        return u'[Newsletter]'

    def send_newsletter(
        self,
        users=None,
        now=None,
        store=True,
        comments=None,
        events=None,
        notifications=None,
        messages=None,
        use_https=False,
    ):

        now = now if now else timezone.now()
        context = {}
        newsletter = self

        # set comments
        comments = newsletter.comments.all() if comments is None else comments

        # get active users
        users = User.objects.members().exclude(
            newsletters__newsletter__in=[newsletter],
        )[:5] if users is None else users

        # check if exists newsletter and users
        if newsletter and users:
            # set data context for emails
            context['comments'] = comments
            # next_events
            next_events = Event.objects.between_dates(
                now,
                now + timezone.timedelta(days=14)
            ) if events is None else events

            for user in users:
                # set user to the context
                context['user'] = user

                # set next events to the context
                context['next_events'] = (
                    next_events
                    if user.is_experimenta()
                    else next_events.exclude(
                        activity_type=Event.ACTIVITY_TYPES.EXPERIMENTA
                    )
                ) if events is None else events

                context['event_colors'] = Event.get_dict_event_colors()
                # set unread notifications to the context
                context['unread_notifications'] = (
                    user.notification_set.filter(
                        read=False,
                    ).count()
                ) if notifications is None else notifications

                # set unread messages to the context
                context['unread_messages'] = (
                    user.received_email_messages.filter(
                        read=False,
                    ).count()

                ) if messages is None else messages

                # add urls vars
                current_site = Site.objects.get_current()
                site_name = current_site.name
                domain = current_site.domain
                protocol = 'https' if use_https else 'http'
                context['site_name'] = site_name
                context['domain'] = domain
                context['protocol'] = protocol

                # send email
                email_manager.send_emails(
                    emails=(user.email,),
                    template_name='newsletter',
                    subject=newsletter.get_subject(),
                    context=context,
                    fail_silently=False,
                )

                # update user's newsletter flag
                if store:
                    if not SentNewsletter.objects.filter(
                        user=user,
                        newsletter=newsletter,
                    ).exists():

                        # add log
                        SentNewsletter.objects.create(
                            user=user,
                            newsletter=newsletter,
                        )

    @classmethod
    def send_todays_newsletter(cls, now=timezone.now()):
        """
        Send newsletter by email to active users
        """
        INITIAL_HOUR = 7
        # FINAL_HOUR = 18
        if now.hour >= INITIAL_HOUR:
            today = timezone.localtime(now).date()
            # get active newsletter
            newsletter = cls.get_newsletter(today)
            # send email
            newsletter.send_newsletter(now=now)


class SentNewsletter(BaseModel):
    """
    This model saves newsletter submission information
    """
    # foreign keys
    user = models.ForeignKey(
        User,
        related_name="newsletters",
        verbose_name=_('user'),
    )

    newsletter = models.ForeignKey(
        Newsletter,
        related_name="send_newsletters",
        verbose_name=_('newsletter'),
    )

    # fields
    sent_at = models.DateTimeField(
        blank=True,
        default=timezone.now
    )

    class Meta:
        unique_together = ("user", "newsletter")

    def __unicode__(self):
        return u'Newsletter {} sent at {}'.format(self.user, self.sent_at)
