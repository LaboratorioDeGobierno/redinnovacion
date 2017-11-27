# -* - coding: utf-8 -*-
""" Enums for the documentation application."""

# django
from django.utils.translation import ugettext_lazy as _


class DynamicContentKinds(object):
    """
    DynamicContent enums
    """
    HTML = 'html'
    GALLERY = 'gallery'
    VIDEO = 'video'
    IMAGE = 'image'

    default = HTML

    choices = (
        (GALLERY, _(u'gallery')),
        (IMAGE, _(u'image')),
        (HTML, _(u'HTML')),
        (VIDEO, _(u'Video')),
    )
