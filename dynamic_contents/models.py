# -*- coding: utf-8 -*-
""" Models for the dynamic_contents application. """
# standard library

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import F
from django.utils.translation import ugettext_lazy as _

# models
from .enums import DynamicContentKinds
from base.models import BaseModel
from cases.models import Case
from documentation.models import Methodology
from documentation.models import Tool
from documents.models import Photo
from users.models import User


class DynamicContent(BaseModel, DynamicContentKinds):
    # foreign keys
    created_by = models.ForeignKey(
        User,
        verbose_name=_('created by'),
    )
    photos = models.ManyToManyField(
        Photo,
        blank=True,
    )
    methodology = models.ForeignKey(
        Methodology,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    tool = models.ForeignKey(
        Tool,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    case = models.ForeignKey(
        Case,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    # required fields
    name = models.CharField(
        _('name'),
        max_length=30,
        blank=True,
    )
    content = models.TextField(
        _('content'),
        blank=True,
        null=True,
    )
    url = models.URLField(
        _('url'),
        max_length=200,
        null=True,
        blank=True,
    )
    kind = models.CharField(
        _('kind'),
        max_length=30,
        choices=DynamicContentKinds.choices,
        default=DynamicContentKinds.default,
        blank=True,
    )
    order = models.PositiveIntegerField(
        default=0,
    )

    # optional fields

    class Meta:
        verbose_name = _('dynamic content')
        verbose_name_plural = _('dynamic contents')
        permissions = (
            ('view_dynamiccontent', _('Can view dynamic content')),
        )
        ordering = ('order',)

    def __str__(self):
        return u'{}: {}'.format(self.get_kind_display(), self.name)

    def get_absolute_url(self):
        """ Returns the canonical URL for the DynamicContent object """
        if self.methodology_id:
            return reverse('methodology_detail', args=(self.methodology_id,))

        if self.tool_id:
            return reverse('tool_detail', args=(self.tool_id,))

        return reverse('case_detail', args=(self.case_id,))

    def get_object(self):
        if self.methodology_id:
            return self.methodology
        elif self.tool_id:
            return self.tool
        elif self.case_id:
            return self.case
        return None

    def save(self, *args, **kwargs):
        if not self.order:
            obj = self.get_object()
            if obj:
                count = obj.dynamiccontent_set.all().count()
                self.order = count + 1
        super(DynamicContent, self).save(*args, **kwargs)

    def get_image(self):
        return self.photos.all().last()

    def replace_order(self, new_order):
        parent = self.get_object()

        contents = parent.dynamiccontent_set.exclude(id=self.id)

        conflict = contents.filter(order=new_order).first()

        if not conflict:
            self.update(order=new_order)
            return

        if self.order < new_order:
            contents.filter(order__lte=new_order).update(
                order=F('order') - 1
            )
        elif self.order > new_order:
            contents.filter(order__gte=new_order).update(
                order=F('order') + 1
            )

        if self.order != new_order:
            self.update(order=new_order)

            i = 1
            for dc in parent.dynamiccontent_set.all():
                dc.update(order=i)
                i += 1
