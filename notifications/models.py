# -*- coding: utf-8 -*-
""" Models for the notifications application. """
# standard library

# django
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

# messaging
from messaging import email_manager

# models
from .enums import NotificationKinds
from base.models import BaseModel
from users.models import User
from events.models import Event


class Notification(BaseModel, NotificationKinds):
    # foreign keys
    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
    )
    from_user = models.ForeignKey(
        User,
        verbose_name=_('user'),
        related_name='created_notifications',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    comment = models.ForeignKey(
        'comments.Comment',
        verbose_name=_('comment'),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    event = models.ForeignKey(
        Event,
        null=True,
        blank=True,
        verbose_name=_('event'),
        on_delete=models.CASCADE,
    )
    # onetoone
    email_message = models.OneToOneField(
        'messaging.EmailMessage',
        null=True,
        blank=True,
        verbose_name=_('email message'),
        on_delete=models.SET_NULL,
    )
    # required fields
    url = models.CharField(
        _('url'),
        max_length=255,
        blank=True,
    )
    kind = models.PositiveIntegerField(
        choices=NotificationKinds.choices
    )
    # optional fields
    text = models.CharField(
        _('text'),
        max_length=255,
        blank=True,
    )
    read = models.BooleanField(
        default=False,
    )

    exclude_on_on_delete_test = ('event', 'comment', 'from_user')

    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
        permissions = (
            ('view_notification', _('Can view notifications')),
        )

    def __unicode__(self):
        return self.text

    def get_absolute_url(self):
        """ Returns the canonical URL for the notification object """
        return reverse('notification_list', args=(self.pk,))

    def is_user_based_notification(self):
        return (
            self.kind == self.MENTION or
            self.kind == self.MESSAGE or
            self.kind == self.RESPONSE
        )

    def get_email_message_count(self):
        """
        Get the number of messages associated with a email notification
        """
        email_message = self.email_message
        if email_message:
            EmailMessage = email_message.__class__
            return EmailMessage.objects.filter(
                from_user_id=email_message.from_user_id,
                to_user_id=email_message.to_user_id,
                read=False,
            ).count()
        return 0

    def send_email(self, request=None, **kwargs):
        if not self.user.profile.send_notifications_by_email:
            return

        # only reminder notifications have emails
        if self.kind != self.REMINDER:
            return

        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        if request and request.is_secure():
            protocol = 'https://'
        else:
            protocol = 'http://'

        translation.activate("es")

        template_name = 'notification'
        template_vars = {
            'domain': domain,
            'notification': self,
            'event': self.event,
            'protocol': protocol,
            'site_name': site_name,
            'user': self.user,
        }
        email_manager.send_emails(
            emails=(self.user.email,),
            template_name=template_name,
            subject=(
                u'¡Pronto será la actividad de la Red!'
            ),
            context=template_vars,
            **kwargs
        )


@receiver(post_save, sender=Notification)
def notification_post_create(sender, instance, created, **kwargs):
    if created:
        instance.send_email()
