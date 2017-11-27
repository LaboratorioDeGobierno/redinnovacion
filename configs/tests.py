from django.core.urlresolvers import reverse

from base.tests import BaseTestCase


class AdminListViewTest(BaseTestCase):

    def setUp(self):
        super(AdminListViewTest, self).setUp()
        self.url = reverse('admin_list_view')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(self.user.is_authenticated(), True)
        self.assertEqual(302, response.status_code)

    def test_get_like_admin(self):
        self.user.is_staff = True
        self.user.save()

        self.user2 = self.create_user()
        self.user2.is_superuser = True
        self.user2.save()

        self.user3 = self.create_user()

        response = self.client.get(self.url)
        self.assertEqual(self.user.is_authenticated(), True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(
            response,
            'configs/admin_list.jade')
        self.assertIn(self.user, response.context['user_list'])
        self.assertNotIn(self.user2, response.context['user_list'])
        self.assertNotIn(self.user3, response.context['user_list'])


class AdminDeleteRedirectViewTest(BaseTestCase):

    def setUp(self):
        super(AdminDeleteRedirectViewTest, self).setUp()
        self.user2 = self.create_user()
        self.url = reverse(
            'admin_delete_redirect_view', kwargs={
                'user_pk': self.user2.pk
            })

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(self.user.is_authenticated(), True)
        self.assertRedirects(
            response, 'http://testserver/admin/login/?next='+self.url)

    def test_get_like_admin(self):
        self.user.is_staff = True
        self.user.save()

        self.user2.is_staff = True
        self.user2.save()

        self.user2.refresh_from_db()
        self.assertTrue(self.user2.is_staff)
        response = self.client.get(self.url)
        self.assertEqual(self.user.is_authenticated(), True)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(
            response, reverse('admin_list_view'))
        self.user2.refresh_from_db()
        self.assertFalse(self.user2.is_staff)
