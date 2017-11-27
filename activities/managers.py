from django.db import models
from django.utils import timezone

from base.managers import QuerySet


class EventQueryset(QuerySet):

    def active(self):
        return self.filter(is_active=True)

    def next_activities(self):
        """
        Filter next activities
        """
        start = timezone.now()
        end = start + timezone.timedelta(days=14)
        return self.filter(
                start_date__range=[start, end],
            ).order_by('start_date')
