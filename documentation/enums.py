# -* - coding: utf-8 -*-
""" Enums for the documentation application."""

# django
from django.utils.translation import ugettext_lazy as _


class DocumentationEnum(object):
    """
    Documentation enums
    """
    METHODOLOGY = 'methodology'
    TOOL = 'tool'
    PUBLICATION = 'publication'

    DEFAULT = METHODOLOGY

    DOCUMENTATION_KIND = (
        (METHODOLOGY, _(u'Methodology')),
        (TOOL, _(u'Tool')),
        (PUBLICATION, _(u'Publication')),
    )
