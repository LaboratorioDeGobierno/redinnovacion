""" This document defines the EventManager class"""

# django
from django.db.models import Q
from django.utils import timezone

from base.managers import QuerySet


class EventQueryset(QuerySet):

    def active(self):
        return self.filter(is_active=True)

    def between_dates(self, start_date, end_date):
        """
        Filter events by date range
        """
        query = Q(start_date__range=(start_date, end_date)) \
            | Q(end_date__range=(start_date, end_date)) \
            | Q(start_date__lt=start_date, end_date__gt=end_date)

        return self.filter(query)

    def incomming(self):
        """
        Filter queryset returning future and active events
        """
        now = timezone.now()
        return self.filter(
            Q(end_date__isnull=True, start_date__lte=now) |
            Q(end_date__gt=now)
        ).active()


class StageQuerySet(QuerySet):
    def get_current_stage(self):
        now = timezone.now()
        return self.filter(
            start_date__lte=now,
            end_date__gte=now,
        ).first()

    def active(self):
        return self.filter(is_active=True)
