""" Admin page configuration for the users app """

# django
from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

# models
from users.models import User, TopicOfInterest, UserProfile

# forms
from users.forms import UserCreationForm
from users.forms import UserChangeForm

# base
from base.admin import download_report

# import export
from import_export.admin import ImportExportModelAdmin

# resources
from users.resources import UserResource


def force_logout(modeladmin, request, queryset):
    for user in queryset:
        user.force_logout()

    # TODO add log to register this action

    messages.add_message(request, messages.SUCCESS,
                         _("Selected users where logged out"))


force_logout.short_description = _("Logs out the user from all devices")


class UserAdmin(DjangoUserAdmin, ImportExportModelAdmin):
    """ Configuration for the User admin page"""
    add_form_template = 'admin/users/user/add_form.html'
    change_form_template = 'admin/users/user/change_form.jade'

    add_form = UserCreationForm
    list_display = (
        'email',
        'first_name',
        'last_name',
        'mother_family_name',
        'institution',
        'other_institution_name',
        'status',
        'is_staff',
        'change_password_link',
        'is_active',
        'send_recover_password_link',
    )
    form = UserChangeForm

    actions = (download_report,)

    search_fields = (
        'first_name',
        'last_name',
        'mother_family_name',
        'email',
    )

    list_filter = (
        'is_active',
        'status',
        'created_at',
        'last_login',
        'platform_attributes__name',
        'platform_attributes__platform',
        'platform_attributes__value',
    )

    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'mother_family_name',
                'institution',
                'region',
                'phone',
                'avatar',
                'interests',
                )}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'status',
            'groups',
            'user_permissions',
        )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'mother_family_name',
                'password1', 'password2',
            ),
        }),
    )
    search_fields = ('first_name', 'last_name', 'mother_family_name', 'email')
    ordering = ('email',)
    filter_horizontal = ('interests',)
    resource_class = UserResource

    def change_password_link(self, obj):
        return u"<a href=\"%d/password/\">%s</a>" % (
            obj.id, _("change password").capitalize())
    change_password_link.allow_tags = True
    change_password_link.short_description = _("change password")

    def send_recover_password_link(self, obj):
        from django.core.urlresolvers import reverse
        return u'<a href="{}">{}</a>'.format(
            reverse('send_recover_password_email', args=(obj.id,)),
            _('send recover password email').capitalize(),
        )
    send_recover_password_link.allow_tags = True
    send_recover_password_link.short_description = _('send recover password email')


admin.site.register(User, UserAdmin)


class TopicOfInterestAdmin(admin.ModelAdmin):
    pass


admin.site.register(TopicOfInterest, TopicOfInterestAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'show_name',
        'show_charge',
        'show_institution',
        'show_email',
        'show_phone',
        'show_interests',
        'time_in_ri',
        'other_topics',
        'show_public_information',
    )

    search_fields = (
        'user__first_name',
        'user__last_name',
        'user__mother_family_name',
        'user__email',
    )


admin.site.register(UserProfile, UserProfileAdmin)
