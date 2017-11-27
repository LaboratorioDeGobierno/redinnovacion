# django
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# models
from .managers import EmailMessageQuerySet
from base.models import BaseModel
from notifications.models import Notification
from users.models import User


class EmailMessage(BaseModel):
    from_user = models.ForeignKey(
        User,
        related_name='sent_email_messages',
    )
    to_user = models.ForeignKey(
        User,
        related_name='received_email_messages',
    )
    subject = models.CharField(
        _('subjet'),
        max_length=255,
        null=True,
        blank=True,
    )
    message = models.TextField(
        _('message'),
        max_length=500,
    )
    read = models.BooleanField(
        default=False,
    )

    objects = EmailMessageQuerySet.as_manager()

    class Meta:
        ordering = ('-id',)

    def __unicode__(self):
        return self.message

    @classmethod
    def group_by_date(cls, email_messages):
        email_messages_by_dates = []

        current_date = None

        for email_message in email_messages:
            if current_date != email_message.created_at.date():
                current_date = email_message.created_at.date()

                email_messages_in_date = []

                email_messages_by_dates.append({
                    'date': current_date,
                    'email_messages': email_messages_in_date,
                })

            email_messages_in_date.append(email_message)

        return email_messages_by_dates


@receiver(post_save, sender=EmailMessage)
def email_message_post_save(sender, instance, created, **kwargs):
    if created and not settings.TEST:
        notification_kwargs = {
            'from_user_id': instance.from_user_id,
            'user_id': instance.to_user_id,
            'kind': Notification.MESSAGE,
            'email_message': instance,
            'read': True,
        }

        Notification.objects.create(**notification_kwargs)
