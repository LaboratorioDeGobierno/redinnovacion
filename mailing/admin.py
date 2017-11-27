# django
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# models
from mailing.models import EmailTemplate
from mailing.models import TemplateImage
from mailing.models import EmailTarget
from mailing.models import Mailing


def send_mailing(modeladmin, request, queryset):
    for obj in queryset:
        obj.send_to_targets()


send_mailing.short_description = _('Send emails for mailing')


def force_mailing(modeladmin, request, queryset):
    for obj in queryset:
        obj.send_to_targets(force=True)


force_mailing.short_description = _(
    _('Force send emails for mailing, independent of its status')
)


def create_and_send_with_mailchimp(modeladmin, request, queryset):
    for obj in queryset:
        obj.create_and_set_using_mailchimp()


create_and_send_with_mailchimp.short_description = _(
    _('Create campaign on mailchimp.'),
)


def create_and_schedule_with_mailchimp(modeladmin, request, queryset):
    for obj in queryset:
        obj.create_and_set_using_mailchimp(default_schedule=True)


create_and_schedule_with_mailchimp.short_description = _(
    _('Create and schedule on mailchimp.'),
)


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at')


admin.site.register(EmailTemplate, EmailTemplateAdmin)


class TemplateImageAdmin(admin.ModelAdmin):
    list_display = ('template', 'image', 'created_at')


admin.site.register(TemplateImage, TemplateImageAdmin)


class EmailTargetAdmin(admin.ModelAdmin):
    list_display = ('platform', 'attribute_name', 'attribute_value')


admin.site.register(EmailTarget, EmailTargetAdmin)


class MailingAdmin(admin.ModelAdmin):
    filter_horizontal = ('targets',)
    list_display = (
        'id',
        'template',
        'get_targets',
        'use_only_active_users',
        'filter_by_user_status',
        'current_target_count',
        'waiting_to_be_sent',
        'scheduled_at',
        'mailing_process_started_at',
    )
    actions = [
        send_mailing,
        force_mailing,
        create_and_schedule_with_mailchimp,
    ]

    def current_target_count(self, obj):
        return obj.get_users().count()


admin.site.register(Mailing, MailingAdmin)
