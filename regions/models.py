# -*- coding: utf-8 -*-

# django
from django.db import models
from django.db.models import Case
from django.db.models import Count
from django.db.models import When
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext_noop

# models
from base.models import BaseModel

# enums
from users.enums import UserEnum

# mark for translation the app name
ugettext_noop("Regions")


class Region(BaseModel):
    name = models.CharField(
        _('name'), max_length=100, unique=True,
        help_text=_('The name of the region'),
    )
    short_name = models.CharField(
        _('short name'), max_length=100,
        null=True, blank=True, unique=True,
        help_text=_('A short name of the region'),
    )
    order = models.IntegerField(
        unique=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = _("regions")
        verbose_name = _("region")
        ordering = ('order',)

    def __unicode__(self):
        return '%s - %s' % (self.short_name, self.name)

    @classmethod
    def get_user_count_by_region(cls):
        """
        Return to an array of regions with users count
        """
        # get data by region, filtering users
        regions = cls.objects.all().prefetch_related('users').annotate(
            users__count=Count(
                Case(
                    When(
                        users__status=UserEnum.STATUS_ACCEPTED,
                        users__is_active=True,
                        then=1,
                    )
                )
            )
        ).order_by(
            '-users__count'
        ).values(
            'users__count',
            'name',
            'order',
        )
        # total users
        total_users = sum([region['users__count'] for region in regions])
        # add percent
        for region in regions:
            region['percent'] = (int(
                round(region['users__count'] * 100.0 / total_users)
            ) if total_users > 0 else 0)

        return regions


class County(BaseModel):
    # foreign keys

    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
    )

    # required fields
    name = models.CharField(
        _('name'), max_length=100, unique=True,
        help_text=_(u'The name of the county'),
    )

    exclude_on_on_delete_test = ('region',)

    class Meta:
        verbose_name_plural = _(u'counties')
        verbose_name = _(u'county')
        ordering = ['name']

    def __unicode__(self):
        return self.name
