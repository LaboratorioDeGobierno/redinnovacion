# -* - coding: utf-8 -*-
""" Enums for the users application."""

# django
from django.utils.translation import ugettext_lazy as _


class UserEnum(object):
    """
    User enums
    """
    STATUS_PENDING = 0
    STATUS_ACCEPTED = 1
    STATUS_REJECTED = 2
    STATUS_OTHER = 3

    STATUS_CHOICES = (
        (STATUS_PENDING, _(u'Pendiente')),
        (STATUS_ACCEPTED, _(u'Aceptado')),
        (STATUS_REJECTED, _(u'Rechazado')),
        (STATUS_OTHER, _(u'Otro')),
    )


class UserProfileEnum(object):
    """
    User profile enums
    """
    TIME_1_WEEK = 0
    TIME_15_DAYS = 1
    TIME_1_MONTH = 2
    TIME_OCCASIONALLY = 3
    TIME_OTHER = 4

    TIME_CHOICES = (
        (TIME_1_WEEK, _(u'Una vez a la semana')),
        (TIME_15_DAYS, _(u'Una vez cada 15 días')),
        (TIME_1_MONTH, _(u'Una vez al mes')),
        (TIME_OCCASIONALLY,
            _(u'Solo algunas veces ocasionales al año')),
        (TIME_OTHER, _(u'Otro')),
    )
