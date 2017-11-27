# -*- coding: utf-8 -*-

# django
from django.contrib.auth.models import Group
from django.core.validators import validate_email
from django.utils import timezone

# import_export
from import_export import fields
from import_export import resources
from import_export import widgets

# models
from users.models import User
from institutions.models import Institution
from platforms.models import Platform
from platforms.models import UserPlatformAttribute


def get_str_group_id_by_name(name):
    """
    Clean name, then returns the id of the group with that name,
    if there is no return None
    """
    # clean name
    name = name.capitalize().strip()
    # query group
    query = Group.objects.filter(name=name)
    # check if exists
    if query.exists():
        # return a string with the group id
        return str(query.first().id)
    return None


def get_str_institution_id_by_name(name):
    """
    Get institution by name
    """
    # get institution
    query = Institution.objects.filter(name=name)
    # check if exists
    if query.exists():
        # return a string with the institution id
        return str(query.first().id)
    return None


class UserResource(resources.ModelResource):
    export_order = ('first_name', 'last_name', 'email')
    import_id_fields = ('email',)

    class Meta:
        model = User
        exclude = [
            'created_at',
            'updated_at',
            'password',
            'last_login',
            'is_superuser',
            'user_permissions',
            'interests',
            'avatar',
            'is_staff',
            'date_joined',
        ]
        export_order = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'address',
            'institution',
            'region',
            'status',
            'is_active',
            'groups',
        ]
        import_id_fields = ('email',)

    def before_import_row(self, row, **kwargs):
        """
        Override to add additional logic. Does nothing by default.
        """
        row['email'] = row['email'].lower().rstrip()

        if row.get('groups', None):
            # get groups names
            group_names = row['groups'].split(',')
            # save the ids of existing groups
            row['groups'] = ','.join(
                filter(None, map(get_str_group_id_by_name, group_names))
            )

        if row.get('institution', None):
            try:
                # first cast int, if institution is an id, then cast str
                # if institution is not an id (can't cast to int),
                # get the id with the name
                row['institution'] = str(int(row['institution']))
            except ValueError:
                row['institution'] = get_str_institution_id_by_name(
                    row['institution']
                )

        validate_email(row['email'])

    def skip_row(self, instance, original):
        """
        Returns True if row importing should be skipped.
        """

        if getattr(self, 'should_skip_row', False):
            return True
        return super(UserResource, self).skip_row(instance, original)

    def after_import_instance(self, instance, new, **kwargs):
        """
        Sets flag for skipping row if its an update
        """

        if new:
            self.should_skip_row = False
        else:
            self.should_skip_row = True

        if instance.created_at is None:
            instance.created_at = timezone.now()
            instance.updated_at = timezone.now()

    def after_import_row(self, row, row_result, **kwargs):
        platform_name = row.get('platform')
        p_attribute_name = row.get('attribute name')
        p_attribute_value = row.get('attribute value')

        if platform_name:
            platform, created = Platform.objects.get_or_create(
                name=platform_name,
            )

        group_id = row.get('groups')
        institution = row.get('institution')
        if (p_attribute_name and p_attribute_value) or group_id or institution:
            user = User.objects.filter(
                email=row.get('email'),
            ).first()

            if not user:
                return

        if p_attribute_name and p_attribute_value:
            UserPlatformAttribute.objects.get_or_create(
                user=user,
                platform=platform,
                name=p_attribute_name,
                value=p_attribute_value,
            )

        if group_id:
            user.groups.add(group_id)

        if institution:
            user.institution_id = institution
            user.save()

    def dehydrate_groups(self, obj):
        """
        Representation of groups at the time of export
        """
        if obj.id:
            groups = obj.groups.all()
            return u", ".join(map(str, groups))

    def dehydrate_institution(self, obj):
        """
        Representation of institution at the time of export
        """
        if obj.id:
            institution = obj.institution
            if institution:
                return u"{}".format(institution.name)
            return u''


class ExportUserResource(resources.ModelResource):
    first_name = fields.Field(
        column_name='Nombre',
        attribute='first_name',
    )
    last_name = fields.Field(
        column_name='Apellido',
        attribute='last_name',
    )
    email = fields.Field(
        column_name='Correo',
        attribute='email',
    )
    charge = fields.Field(
        column_name='Cargo',
        attribute='charge',
    )
    region = fields.Field(
        column_name=u'Región',
        attribute='region',
        widget=widgets.ForeignKeyWidget(User, 'region')
    )
    institution = fields.Field(
        column_name=u'Institución',
        attribute='institution',
        widget=widgets.ForeignKeyWidget(User, 'institution')
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'institution',
            'region',
            'charge',
        )
        export_order = (
            'first_name',
            'last_name',
            'email',
            'institution',
            'region',
            'charge'
        )

    def dehydrate_institution(self, obj):
        """
        Representation of institution at the time of export
        """
        if obj.id:
            institution = obj.institution
            if institution:
                return u"{}".format(institution.name)
            return u''

    def dehydrate_region(self, obj):
        """
        Representation of region at the time of export
        """
        if obj.id:
            region = obj.region
            if region:
                return u"{}".format(region.name)
            return u''
