# -* - coding: utf-8 -*-
""" Models for the users application.

All apps should use the users.User model for all users
"""

import random
import string

# django
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sessions.models import Session
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator

from rest_framework.authtoken.models import Token
from phonenumber_field.modelfields import PhoneNumberField

from easy_thumbnails.fields import ThumbnailerImageField

# managers
from users.managers import UserManager

# models
from base.models import BaseModel, file_path

# messaging
from messaging import email_manager

# enums
from users.enums import UserEnum
from users.enums import UserProfileEnum

# utils
from users.utils import calculate_slug

# standard library

# faker
from faker import Faker

# mark for translation the app name
ugettext_noop("Users")


class User(AbstractBaseUser, PermissionsMixin, BaseModel, UserEnum):
    """
    User model with admin-compliant permissions, and BaseModel characteristics

    Email and password are required. Other fields are optional.
    """

    # foreign keys
    region = models.ForeignKey(
        'regions.Region',
        verbose_name=_('region'),
        related_name='users',
        null=True,
        on_delete=models.SET_NULL,
    )
    county = models.ForeignKey(
        'regions.County',
        verbose_name=_('county'),
        related_name='users',
        null=True,
        on_delete=models.SET_NULL,
    )

    # required fields
    email = models.EmailField(
        _('email address'), unique=True, db_index=True,
    )
    # optional fields
    first_name = models.CharField(
        _('first name'), max_length=30, blank=False,
        validators=[MinLengthValidator(2)]
    )
    last_name = models.CharField(
        _('last name'), max_length=30, blank=False,
        validators=[MinLengthValidator(2)]
    )
    mother_family_name = models.CharField(
        _('mother family name'), max_length=30,
        blank=True, null=True,
    )
    charge = models.CharField(
        _('charge'),
        max_length=150,
        null=True,
    )
    phone = PhoneNumberField(
        _('phone'),
        null=True,
    )
    address = models.CharField(
        _('address'),
        max_length=255,
        null=True,
    )
    city = models.CharField(
        _('address'),
        max_length=255,
        null=True,
    )
    institution = models.ForeignKey(
        'institutions.Institution',
        verbose_name=_('institution'),
        related_name='users',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    other_institution_name = models.CharField(
        blank=True,
        null=True,
        max_length=32,
        verbose_name=_('other institution name'),
    )
    avatar = ThumbnailerImageField(
        _('avatar'),
        upload_to=file_path,
        blank=True,
        null=True,
    )
    description = models.TextField(
        _('description'),
        null=True,
        max_length=750,
    )
    status = models.PositiveSmallIntegerField(
        _('status'),
        choices=UserEnum.STATUS_CHOICES,
        default=UserEnum.STATUS_PENDING,
    )
    interests = models.ManyToManyField(
        'interests.Interest',
        related_name='users',
        verbose_name=_('interests'),
        blank=True,
    )

    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'),
    )
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'),
    )
    # auto fields
    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now,
        help_text=_("The date this user was created in the database"),
    )
    token = models.CharField(
        _('token'),
        max_length=30,
        default="",
        blank=True,
        help_text="A token that can be used to verify the user's email"
    )
    slug = models.SlugField(
        _('slug'),
        max_length=100,
        unique=True,
        null=True,
        blank=True,
    )
    last_activity = models.DateTimeField(
        _('last activity'), default=timezone.now,
        help_text=_("The datetime of the last activity performed by the user"),
    )
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    exclude_on_on_delete_test = ('region',)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.get_full_name()

    # public methods
    def get_avatar_url(self):
        """
        Returns the url of this user's avatar. Returns None if it
        has no image uploaded.
        """
        if not self.avatar:
            return static('img/people.svg')
        return self.avatar.url

    def get_absolute_url(self):
        if self.slug:
            return reverse('participant_detail', kwargs={
                'slug': self.slug,
            })
        else:
            return reverse('participant_detail', kwargs={
                'pk': self.id,
            })

    def get_message_url(self):
        if self.slug:
            return reverse(
                'email_message_list', kwargs={
                    'slug': self.slug,
                }
            )

        return reverse(
            'email_message_list_by_pk', kwargs={
                'user_pk': self.pk,
            }
        )

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_liked_comment_ids(self):
        return self.commentlike_set.values_list('comment_id', flat=True)

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def get_recover_password_url(self, request=None):

        uid = urlsafe_base64_encode(force_bytes(self.pk))
        token = default_token_generator.make_token(self)

        protocol = 'http'
        if request and request.is_secure():
            protocol = 'https'

        current_site = get_current_site(request)
        domain = current_site.domain

        return '{}://{}{}'.format(
            protocol,
            domain,
            reverse('users.views.password_reset_confirm', kwargs={
                'uidb64': uid,
                'token': token,
            }),
        )

    def save(self, *args, **kwargs):
        """
        Overridden to ensure that before record is saved:
        * email is lowercase
        * first and last name don't have leading or trailing whitespace
        * slug is not empty
        """
        self.email = self.email.lower()
        self.first_name = self.first_name.strip() if self.first_name else ""
        self.last_name = self.last_name.strip() if self.last_name else ""
        self.mother_family_name = (
            self.mother_family_name.strip() if self.mother_family_name else ""
        )

        if (
            not self.slug
            and self.is_active
            and self.status == UserEnum.STATUS_ACCEPTED
        ):
            self.slug = calculate_slug(
                self.first_name,
                self.last_name,
                self.mother_family_name,
                self.email,
                User
            )

        super(User, self).save(*args, **kwargs)

    def send_example_email(self):
        email_manager.send_example_email(self.email)

    def send_recover_password_email(self, request=None):
        """
        Sends an email with the required token so a user can recover
        his/her password
        """
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        protocol = 'http'
        if request and request.is_secure():
            protocol = 'https'

        template_vars = {
            'email': self.email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(self.pk)),
            'user': self,
            'token': default_token_generator.make_token(self),
            'protocol': protocol,
        }

        template_name = 'password_reset'
        subject = 'Clave restablecida en Red'
        email_manager.send_emails(
            emails=(self.email,),
            template_name=template_name,
            subject=subject,
            context=template_vars,
        )

    def send_email_message(self, request, subject, message, **kwargs):
        return self.received_email_messages.create(
            from_user=request.user,
            message=message,
        )

    def send_activate_email(self, request=None):
        if self.is_active:
            template_name = 'user_activation'
        else:
            template_name = 'external_acceptance'
        subject = 'Tu cuenta ha sido aceptada'
        return self.send_email(
            request,
            template_name=template_name,
            subject=subject,
        )

    def send_rejection_email(self, request=None):
        template_name = 'user_rejection'
        subject = 'Tu cuenta ha sido rechazada'
        return self.send_email(
            request,
            template_name=template_name,
            subject=subject,
        )

    def send_email(
        self,
        request=None,
        template_name='example_email',
        subject='Hola',
        template_vars=None,
        **kwargs
    ):

        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        protocol = 'http'
        if request and request.is_secure():
            protocol = 'https'

        if template_vars is None:
            template_vars = {}

        template_vars.update({
            'email': self.email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(self.pk)),
            'user': self,
            'token': default_token_generator.make_token(self),
            'protocol': protocol,
        })

        email_manager.send_emails(
            emails=(self.email,),
            subject=subject,
            template_name=template_name,
            context=template_vars,
            **kwargs
        )

    def send_activity_inscription_email(self, request, activity, **kwargs):
        template_name = 'activity_inscription'
        subject = (
            u'Te has inscrito a una actividad de la '
            u'Red'
        )
        template_vars = {
            'event': activity.event,
        }
        self.send_email(
            request,
            template_name=template_name,
            subject=subject,
            template_vars=template_vars,
            **kwargs
        )

    def force_logout(self):
        """
        Deletes all the sessions of the User
        """
        # delete all the sessions that match the user
        for s in Session.objects.all():
            pk = s.get_decoded().get('_auth_user_id')
            if pk and int(pk) == self.id:
                s.delete()

    def set_token(self, commit=True):
        """ generate a random token """
        chars = string.ascii_uppercase + string.digits

        token = "{}-{}".format(
            ''.join(random.choice(chars) for x in range(10)),
            ''.join(random.choice(chars) for x in range(19))
        )
        self.token = token

        if commit:
            self.save()

        return token

    def is_experimenta(self):
        experimenta = Group.objects.filter(name="Experimenta").first()
        return experimenta in self.groups.all()

    @classmethod
    def experimenta_users(cls):
        experimenta = Group.objects.filter(name="Experimenta").first()
        return cls.objects.filter(groups__in=[experimenta, ])

    def is_member(self):
        return self.is_active and self.status == UserEnum.STATUS_ACCEPTED

    @classmethod
    def generate(cls, quantity):
        fake = Faker()
        DEFAULT_AVATAR_URL = ''
        users = []
        for e in range(quantity):
            user = {
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'get_full_name': fake.name(),
                'email': fake.email(),
                'is_active': True,
                'avatar': {
                    'url': DEFAULT_AVATAR_URL,
                },
            }
            users.append(user)

        return users

    def is_pending(self):
        return self.status == UserEnum.STATUS_PENDING

    def is_accepted(self):
        return self.status == UserEnum.STATUS_ACCEPTED and self.is_active

    def get_last_message(self, user):
        sent = self.sent_email_messages.filter(to_user=user)
        received = self.received_email_messages.filter(from_user=user)
        return (sent | received).order_by('-created_at').first()


class UserProfile(BaseModel, UserProfileEnum):

    user = models.OneToOneField(
        User,
        related_name='profile',
        verbose_name=_('user'),
        null=True,
        on_delete=models.CASCADE,
    )
    show_name = models.BooleanField(
        _('show name'),
        default=True,
    )
    show_charge = models.BooleanField(
        _('show charge'),
        default=True,
    )
    show_institution = models.BooleanField(
        _('show institution'),
        default=True,
    )
    show_email = models.BooleanField(
        _('show email'),
        default=True,
    )
    show_phone = models.BooleanField(
        _('show phone'),
        default=True,
    )
    show_interests = models.BooleanField(
        _('show interests'),
        default=True,
    )
    send_notifications_by_email = models.BooleanField(
        _('send notifications by email'),
        default=True,
    )

    time_in_ri = models.PositiveSmallIntegerField(
        _('time in ri'),
        choices=UserProfileEnum.TIME_CHOICES,
        null=True,
        blank=False,
        default=None,
    )
    topic_of_interests = models.ManyToManyField(
        'TopicOfInterest',
        verbose_name=_('topic of interests'),
        related_name='user_profile',
        blank=False,
    )
    other_topics = models.CharField(
        blank=True,
        max_length=140,
        null=True,
        verbose_name=_('other topics'),
    )
    show_public_information = models.NullBooleanField(
        _('show public information'),
        choices=BaseModel.BOOLEAN_CHOICES,
        null=True,
        blank=False,
        default=None,
    )
    imported = models.BooleanField(default=False)

    exclude_on_on_delete_test = ('user',)

    def __unicode__(self):
        return self.user.get_full_name()

    def get_absolute_url(self):
        return reverse(
            'user_profile'
        )


class TopicOfInterest(BaseModel):
    topic = models.CharField(
        _('topic'),
        max_length=50,
    )
    order = models.PositiveSmallIntegerField(
        _('order'),
        default=0,
    )

    def clean(self):
        self.topic = self.topic.strip()

    class Meta:
        ordering = ('order', 'topic')

    def __unicode__(self):
        return self.topic


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        Token.objects.create(user=instance)
