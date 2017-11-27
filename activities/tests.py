# -*- coding: utf-8 -*-
#
from django.utils import timezone
from django.core.urlresolvers import reverse

from base.tests import BaseTestCase
from activities.models import UserActivity
from events.models import Stage, UserEvent


class GoogleCalendarLinkTest(BaseTestCase):

    def test_google_calendar_link(self):
        event = self.create_event(
            name=u'Taller de Introducción a la Innovación',
        )
        activity = self.create_activity(
            event=event,
            address=u"Calle de la Innovación",
            city=u"Ciudad de la Innovación",
            description=u"Descripción de la Innovación",
            region=self.create_region(),
            start_date=timezone.now().date(),
            end_date=timezone.now().date(),
        )
        activity.get_calendar_url()


class UserActivityTest(BaseTestCase):

    def test_attend(self):
        user_activity = self.create_user_activity()
        self.assertIsNone(user_activity.attendance_date)

        user_activity.attend()
        self.assertIsNotNone(user_activity.attendance_date)

        now = timezone.now()
        user_activity.attend(now)
        self.assertEqual(user_activity.attendance_date, now)


class ActivityTest(BaseTestCase):

    def test_deactivate(self):
        activity = self.create_activity(is_active=True)
        self.assertTrue(activity.is_active)
        activity.deactivate()
        self.assertFalse(activity.is_active)

    def test_register_attendant(self):
        activity = self.create_event(quota=None).get_base_activity()
        registered, error = activity.register_assistant(self.user)
        self.assertFalse(registered)
        self.assertTrue(error)

        activity = self.create_event(quota=0).get_base_activity()
        registered, error = activity.register_assistant(self.user)
        self.assertFalse(registered)
        self.assertTrue(error)

        activity = self.create_event(quota=100).get_base_activity()
        registered, error = activity.register_assistant(self.user)
        self.assertTrue(registered)
        self.assertIsNone(error)
        self.assertEquals(activity.quota, 99)

        stage = Stage.objects.filter(event=activity.event)
        stage = stage.filter(stage_type=Stage.STAGE_TYPE_INSCRIPTION).first()
        useractivities = UserActivity.objects.filter(activity=activity)
        useractivities = useractivities.filter(user=self.user, stage=stage)
        userevents = UserEvent.objects.filter(event=activity.event)
        userevents = userevents.filter(user=self.user)

        self.assertIsNotNone(stage)
        self.assertIsNotNone(useractivities.first())
        self.assertIsNotNone(userevents.first())


class UserActivityCreateViewTest(BaseTestCase):

    def setUp(self):
        super(UserActivityCreateViewTest, self).setUp()
        self.activity = self.create_activity()
        kwargs = {
            'pk': self.activity.pk,
        }
        self.url = reverse('user_activity_create', kwargs=kwargs)
        self.success_url = reverse('activity_detail', kwargs=kwargs)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response, self.success_url, target_status_code=302)
