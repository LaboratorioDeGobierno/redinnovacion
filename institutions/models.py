from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from base.models import BaseModel, file_path
from easy_thumbnails.fields import ThumbnailerImageField

from .managers import InstitutionQueryset


class InstitutionKind(BaseModel):
    name = models.CharField(
        _('name'),
        max_length=100,
        unique=True
    )

    def __unicode__(self):
        return self.name


class Institution(BaseModel):
    name = models.CharField(
        _('name'),
        max_length=255,
    )
    url = models.URLField(
        _('url'),
        null=True,
        blank=True,
    )
    address = models.CharField(
        _('address'),
        max_length=255,
        null=True,
        blank=True,
    )
    phone = PhoneNumberField(
        _('phone'),
        null=True,
        blank=True,
    )
    role_description = models.TextField(
        _('role description'),
        max_length=500,
        null=True,
        blank=True,
    )
    logo = ThumbnailerImageField(
        _('logo'),
        upload_to=file_path,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        _('is active'),
        default=True,
    )
    imported = models.BooleanField(default=False)
    slug = models.SlugField(
        _('slug'),
        unique=True,
        max_length=100,
        null=True,
    )

    # foreign keys
    kind = models.ForeignKey(
        InstitutionKind,
        verbose_name=_('institution kind'),
        related_name='institutions',
        null=True,
        on_delete=models.SET_NULL,
    )

    objects = InstitutionQueryset.as_manager()
    prepopulated_fields = {
        'slug': ('first_name', 'last_name'),
    }

    class Meta:
        unique_together = ('name', 'address')
        ordering = ('name',)

    @property
    def users_count(self):
        from users.models import User
        return self.users.filter(status=User.STATUS_ACCEPTED).count()

    def __unicode__(self):
        return self.name

    @classmethod
    def report_by_kind(cls):
        from users.models import User

        report = []

        total_users = 0
        for kind in InstitutionKind.objects.all():
            users_count = User.objects.members().filter(
                institution__kind=kind
            ).count()
            total_users += users_count

            report.append({
                'id': kind.id,
                'count': cls.objects.filter(kind=kind).count(),
                'name': kind.name,
                'users__count': users_count,
            })

        if total_users:
            for rep in report:
                rep['percent'] = rep['users__count'] * 100 / total_users
        else:
            for rep in report:
                rep['percent'] = 0

        return report

    def get_absolute_url(self):
        return reverse(
            'institution_detail', kwargs={
                'slug': self.slug,
            }
        )

    def save(self, *args, **kwargs):
        # if slug is not define or already exists, create a new one
        if (
            (not self.slug and self.name)
            or Institution.objects.filter(slug=self.slug).exists()
        ):
            self.slug = slugify(self.name)
            i = 1
            while Institution.objects.filter(slug=self.slug).exists():
                self.slug = '{}-{}'.format(slugify(self.name), i)
                i += 1
        super(Institution, self).save(*args, **kwargs)
