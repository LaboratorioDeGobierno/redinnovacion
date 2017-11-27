""" This document defines the EmailMessageManager class"""

# django
from django.db.models import Q

# base
from base.managers import QuerySet


class EmailMessageQuerySet(QuerySet):

    def filter_by_user(self, user):
        return self.filter(Q(from_user=user) | Q(to_user=user))
