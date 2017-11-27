from django.db import models
from django.utils.translation import ugettext_lazy as _

from base.models import BaseModel


class Interest(BaseModel):
    interest = models.CharField(
        _('interest'),
        max_length=50
    )
    order = models.PositiveSmallIntegerField(
        _('order'),
        default=0,
    )

    class Meta:
        ordering = ('order', 'interest',)

    def __unicode__(self):
        return self.interest
