# stdlib
from uuid import uuid4
from base64 import b64encode

# django
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

# models
from base.models import BaseModel
from users.models import User


class Platform(BaseModel):
    # required fields
    name = models.CharField(
        _('name'),
        max_length=255,
        unique=True,
    )
    token = models.CharField(
        _('token'),
        max_length=255,
    )

    class Meta:
        verbose_name_plural = _('platforms')
        verbose_name = _('platform')
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def reset_token(self):
        self.token = b64encode(uuid4().hex)
        self.save()


class UserPlatformAttribute(BaseModel):
    user = models.ForeignKey(
        User,
        related_name='platform_attributes',
    )
    platform = models.ForeignKey(
        'Platform',
        related_name='platform_attributes',
    )
    name = models.CharField(
        _('name'),
        max_length=255,
    )
    value = models.CharField(
        _('value'),
        max_length=255,
    )

    class Meta:
        verbose_name_plural = _('user platform attributes')
        verbose_name = _('user platform attribute')
        unique_together = ('user', 'platform', 'name')

    def __unicode__(self):
        return "{}: {}".format(self.name, self.value)


@receiver(post_save, sender=Platform)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        instance.reset_token()


@receiver(post_save, sender=UserPlatformAttribute)
def create_email_target(sender, instance=None, created=False, **kwargs):
    if created:
        from mailing.models import EmailTarget
        EmailTarget.objects.get_or_create(
            platform=instance.platform,
            attribute_name=instance.name,
            attribute_value=instance.value,
        )
