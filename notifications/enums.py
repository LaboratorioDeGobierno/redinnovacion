# django
from django.utils.translation import ugettext_lazy as _


class NotificationKinds(object):
    MENTION = 1
    RESPONSE = 2
    REMINDER = 3
    MESSAGE = 4
    EVENT = 5

    choices = (
        (MENTION, _('MENTION')),
        (RESPONSE, _('RESPONSE')),
        (REMINDER, _('REMINDER')),
        (MESSAGE, _('MESSAGE')),
        (EVENT, _('EVENT')),
    )
