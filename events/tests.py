from base.tests import BaseTestCase
from events.models import Event
from django.utils.timezone import now

from datetime import timedelta


class EventQueriesTest(BaseTestCase):
    model = Event

    def test_active(self):
        event1 = self.create_event(is_active=True)
        event2 = self.create_event(is_active=False)
        queryset = self.model.objects.active()
        self.assertTrue(queryset)
        self.assertIn(event1, queryset)
        self.assertNotIn(event2, queryset)

    def test_incomming(self):
        today = now()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)
        event1 = self.create_event(is_active=True, end_date=yesterday)
        event2 = self.create_event(is_active=True, end_date=tomorrow)
        event3 = self.create_event(is_active=False)

        queryset = self.model.objects.incomming()
        self.assertTrue(queryset)
        self.assertNotIn(event1, queryset)
        self.assertIn(event2, queryset)
        self.assertNotIn(event3, queryset)
