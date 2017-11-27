# -*- coding: utf-8 -*-
# standard
import uuid
import logging
import json

# django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.encoding import smart_str

# ckeditor
from ckeditor_uploader.fields import RichTextUploadingField

# models
from base.models import BaseModel
from jsonfield import JSONField
from users.models import User
from platforms.models import Platform

# enums
from users.enums import UserEnum

# messaging
from messaging import email_manager

# mailchimp client
from mailing.mailchimp import MailchimpAPIClient


def image_file_path(instance, filename):
    """ Returns a file path for a file """
    model_name = instance.__class__.__name__.lower()
    _hash = uuid.uuid4().hex

    return u"{}/{}/{}".format(model_name, _hash, filename)


NOT_SENT = 0
SENT = 1
ERROR = 2
OTHER = 3


class EmailTemplate(BaseModel):
    """ Stores an email template """
    subject = models.CharField(
        max_length=255,
    )
    text_content = models.TextField(
        null=True,
        blank=True,
    )
    html_header = RichTextUploadingField(
        null=True,
        blank=True,
    )
    html_body = models.TextField(
    )
    html_footer = RichTextUploadingField(
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.html_body = smart_str(
            self.html_body
        ).replace('\n', '').replace('\r', '')
        super(EmailTemplate, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.subject

    def make_html_template(self):
        return self.html_header + self.html_body + self.html_footer


class TemplateImage(BaseModel):
    template = models.ForeignKey(
        'EmailTemplate',
        related_name='images',
    )
    image = models.ImageField(
        upload_to=image_file_path,
    )

    def __unicode__(self):
        return self.template.subject


class EmailTarget(BaseModel):
    """
    Stores the instruction to send an email to the users
    that fulfill the given rule.
    """

    platform = models.ForeignKey(
        Platform,
        related_name='email_targets',
    )
    attribute_name = models.CharField(
        max_length=255,
    )
    attribute_value = models.CharField(
        max_length=255,
    )

    def get_users(self):
        return User.objects.filter(
            platform_attributes__name=self.attribute_name,
            platform_attributes__value=self.attribute_value,
        )

    def get_mailing_list(self):
        return self.get_users().values_list('email', flat=True)

    def __unicode__(self):
        return _(u'{}, {}, {}').format(
            self.platform,
            self.attribute_name,
            self.attribute_value
        )


class Mailing(BaseModel):
    # foreign keys
    template = models.ForeignKey(
        'EmailTemplate',
        related_name='mailings',
    )
    targets = models.ManyToManyField(
        'EmailTarget',
        blank=True,
    )
    event = models.ForeignKey(
        'events.Event',
        related_name='mailing',
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )
    # filters
    use_only_active_users = models.BooleanField(
        default=False,
    )
    filter_by_user_status = models.PositiveSmallIntegerField(
        choices=((None, ''),) + UserEnum.STATUS_CHOICES,
        blank=True,
        null=True,
    )
    # optional fields
    waiting_to_be_sent = models.BooleanField(
        default=False,
    )
    scheduled_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    mailing_process_started_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
    )

    def __unicode__(self):
        return u"Mailing {}, subject {}.".format(
            self.id,
            self.template,
        )

    def get_targets(self):
        targets = self.targets.all()
        return ', '.join([unicode(target) for target in targets])

    def create_and_set_using_mailchimp(self, default_schedule=False):
        # list creation and email list subscription
        if not hasattr(self, 'mailchimp_list'):
            self.create_mailchimp_list()
            self.sub_target_users_to_list()
        else:
            self.sub_target_users_to_list(update_existing=True)

        # create campaign
        if not hasattr(self.mailchimp_list, 'mailchimp_list_campaign'):
            self.create_mailchimp_campaign()

        # set campaign content
        response = self.create_mailchimp_campaign_content()

        # mark this campaign to be ready to be sent
        self.waiting_to_be_sent = True
        self.mailing_process_started_at = timezone.now()
        self.save()

        return response

    def get_email_list(self):
        emails = []
        for user in self.get_users():
            emails.append(user.email)
        return emails

    def create_mailchimp_list(self):
        mc = MailchimpAPIClient()
        response = mc.create_list(self.template.subject)

        if response['id']:
            list_obj = MailChimpList.objects.get_or_create(
                external_id=response['id'],
                mailing=self,
                raw_response=json.dumps(response),
            )

            # TODO: Remove hardcoded merge field creation
            eventlink_data = {
                'name': 'Event Invitation Link',
                'tag': 'EVENTLINK',
                'type': 'url',
            }
            mc.create_list_merge_field(response['id'], eventlink_data)

            activity_list_data = {
                'name': 'Activity List',
                'tag': 'ACTIVITIES',
                'type': 'text',
            }
            mc.create_list_merge_field(response['id'], activity_list_data)

            userlink_data = {
                'name': 'User password Link',
                'tag': 'RECOVER_PA',
                'type': 'url',
            }
            mc.create_list_merge_field(response['id'], userlink_data)

        return list_obj

    def sub_target_users_to_list(self, update_existing=False):
        list_id = self.mailchimp_list.external_id
        mc = MailchimpAPIClient()

        def extra_data(fields, user):
            if self.event:
                fields['EVENTLINK'] = self.event.get_invitation_link(user)
                fields['ACTIVITY_LIST'] = \
                    self.event.get_activities_list_html(user)

            fields['RECOVER_PA'] = user.get_recover_password_url()

        response = mc.sub_users_to_list(
            self.get_users(),
            list_id,
            extra_data,
            update_existing=update_existing,
        )
        return response

    def get_users(self):
        users = User.objects.all()

        if self.use_only_active_users:
            users = users.filter(is_active=True)

        if self.filter_by_user_status is not None:
            users = users.filter(status=self.filter_by_user_status)

        if self.targets.exists():
            return users.filter(
                platform_attributes__name__in=self.targets.all(
                ).values_list('attribute_name', flat=True),
                platform_attributes__value__in=self.targets.all(
                ).values_list('attribute_value', flat=True),
            ).distinct()

        return users

    def create_mailchimp_campaign(self):
        mc = MailchimpAPIClient()
        response = mc.create_campaign(self.template, self.mailchimp_list)
        if response['id']:
            MailChimpCampaign.objects.get_or_create(
                external_id=response['id'],
                mailing_list=self.mailchimp_list,
                raw_response=json.dumps(response),
            )
        return response

    def create_mailchimp_campaign_content(self):
        mc = MailchimpAPIClient()

        template = self.template
        campaign = self.mailchimp_list.mailchimp_list_campaign
        response = mc.create_campaign_content(
            template,
            campaign,
        )

        return response

    def send_using_mailchimp(self):
        mc = MailchimpAPIClient()
        response = mc.campaign_send(
            self.mailchimp_list.mailchimp_list_campaign
        )
        return response

    def schedule_using_mailchimp(self, schedule_datetime=None):
        mc = MailchimpAPIClient()
        if not schedule_datetime:
            schedule_datetime = timezone.now()

        response = mc.campaign_schedule(
            self.mailchimp_list.mailchimp_list_campaign,
            time=schedule_datetime,
        )
        return response

    def send_to_targets(self, sender=None, force=False):
        for user in self.get_users():
            target_status = self.get_or_create_target_status(user, force)
            if not target_status:
                logger = logging.getLogger(
                    'mailing.mailtarget.send_to_targets'
                )
                logger.error('Target status different from NOT_SENT')
                continue

            context = {
                'user': user,
                'template': self.template,
            }

            try:
                email_manager.send_emails(
                    emails=(user.email,),
                    template_object=self.template,
                    subject=self.template.subject,
                    context=context,
                    fail_silently=False,
                )

                target_status.status = SENT
                target_status.sent_at = timezone.now()
                target_status.save()
            except Exception as e:
                logger = logging.getLogger(
                    'mailing.mailtarget.send_to_targets'
                )
                logger.error(e)
                target_status.status = ERROR
                target_status.save()

    def get_or_create_target_status(self, user, force=False):
        target, created = EmailStatus.objects.get_or_create(
            user=user,
            mailing=self,
        )

        if force:
            return target

        if target.status is not NOT_SENT:
            return None
        else:
            return target

    get_targets.short_description = _('Targets')


class EmailStatus(BaseModel):
    STATUSES = (
        (NOT_SENT, _('Not Sent')),
        (SENT, _('Sent')),
        (ERROR, _('Error')),
        (OTHER, _('Other')),
    )

    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
    )
    mailing = models.ForeignKey(
        'Mailing',
        related_name='target_statuses',
    )
    status = models.IntegerField(
        _('status'),
        default=0,
        choices=STATUSES,
    )
    sent_at = models.DateTimeField(
        _('sent at'),
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return u"Status {} for mailing: {}".format(self.status, self.mailing)


class MailChimpList(BaseModel):
    mailing = models.OneToOneField(
        'Mailing',
        verbose_name=_('mailing'),
        on_delete=models.CASCADE,
        related_name='mailchimp_list',
    )
    external_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    raw_response = JSONField(
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return self.external_id

    def get_mailchimp_data(self):
        list_id = self.external_id
        mc = MailchimpAPIClient()
        return mc.get_list(list_id)


class MailChimpCampaign(BaseModel):
    external_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    mailing_list = models.OneToOneField(
        'MailChimpList',
        verbose_name=_('mailing list'),
        related_name='mailchimp_list_campaign',
    )
    raw_response = JSONField(
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return self.external_id
