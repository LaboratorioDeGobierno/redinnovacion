"""
Tests for the user app
"""
from django.core.urlresolvers import reverse
from base.tests import BaseTestCase
from users.models import User
from users.forms import UserForm


class UserTests(BaseTestCase):
    def test_lower_case_emails(self):
        """
        Tests that users are created with lower case emails
        """
        self.user.email = "Hello@correo.cl"
        self.user.save()
        self.assertEqual(self.user.email, 'hello@correo.cl')

    def test_force_logout(self):
        """
        Tests that users are created with lower case emails
        """
        url = reverse('password_change')
        response = self.client.get(url)

        # test that the user is logged in
        self.assertEqual(response.status_code, 200)

        self.user.force_logout()

        response = self.client.get(url)

        # user is logged out, sow redirects to login
        self.assertEqual(response.status_code, 302)


class ParticipantsListView(BaseTestCase):

    def setUp(self):
        super(ParticipantsListView, self).setUp()
        self.url = reverse('people_list')
        self.user2 = self.create_user()

    def test_get(self):
        self.user.status = User.STATUS_ACCEPTED
        self.user.save()

        response = self.client.get(self.url)
        self.assertEqual(self.user.is_authenticated(), True)
        self.assertEqual(200, response.status_code)
        self.assertIn(self.user, response.context['object_list'])

    def test_get_user(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'activity/most_active_users.jade')
        self.assertNotIn('pending_user_list', response.context)


class AcceptUserRedirectViewTest(BaseTestCase):

    def setUp(self):
        super(AcceptUserRedirectViewTest, self).setUp()
        self.user2 = self.create_user(is_active=False)
        self.url = reverse(
            'accept_staff_user_redirect_view', kwargs={
                'user_pk': self.user2.pk,
            })
        self.success_url = reverse('pending_participant_list')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(self.user.is_authenticated(), True)
        self.assertRedirects(
            response, 'http://testserver/admin/login/?next=' + self.url)

    def test_get_like_admin(self):
        self.user.is_staff = True
        self.user.save()

        self.assertFalse(self.user2.is_active)
        self.assertEqual(self.user2.status, User.STATUS_PENDING)
        response = self.client.get(self.url)
        self.assertEqual(self.user.is_authenticated(), True)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, self.success_url)
        self.user2.refresh_from_db()
        self.assertTrue(self.user2.is_active)
        self.assertEqual(self.user2.status, User.STATUS_ACCEPTED)


class RejectUserRedirectViewTest(BaseTestCase):

    def setUp(self):
        super(RejectUserRedirectViewTest, self).setUp()
        self.user2 = self.create_user(is_active=False)
        self.url = reverse(
            'reject_user_redirect_view', kwargs={
                'user_pk': self.user2.pk,
            })

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(self.user.is_authenticated(), True)
        self.assertRedirects(
            response, 'http://testserver/admin/login/?next=' + self.url)

    def test_get_like_admin(self):
        self.user.is_staff = True
        self.user.save()

        self.assertFalse(self.user2.is_active)
        self.assertEqual(self.user2.status, User.STATUS_PENDING)
        response = self.client.get(self.url)
        self.assertEqual(self.user.is_authenticated(), True)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(
            response, reverse('participant_list'))
        self.user2.refresh_from_db()
        self.assertFalse(self.user2.is_active)
        self.assertEqual(self.user2.status, User.STATUS_REJECTED)

    # def test_get_user_not_exists(self):
    #     url = reverse(
    #         'reject_user_redirect_view', kwargs={
    #             'user_pk': User.objects.last().pk + 1,
    #         })
    #     response = self.client.get(url)
    #     self.assertTrue(self.user.is_authenticated())
    #     self.assertEqual(404, response.status_code)


class DeleteAccountRedirectViewTest(BaseTestCase):

    def setUp(self):
        super(DeleteAccountRedirectViewTest, self).setUp()
        self.user.status = User.STATUS_ACCEPTED
        self.user.save()
        self.url = reverse(
            'delete_account_redirect_view', kwargs={
                'user_pk': self.user.pk,
            })

    def test_get(self):
        self.assertTrue(self.user.is_active)
        self.assertEqual(self.user.status, User.STATUS_ACCEPTED)

        response = self.client.get(self.url)
        self.assertTrue(self.user.is_authenticated())
        self.assertEqual(302, response.status_code)
        self.assertEqual(response.url, 'http://testserver/')
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        # self.assertFalse(self.user.is_authenticated())

    def test_get_user_not_exists(self):
        user_pk = User.objects.last().pk + 1
        url = reverse(
            'delete_account_redirect_view', kwargs={
                'user_pk': user_pk,
            })
        response = self.client.get(url)
        self.assertTrue(self.user.is_authenticated())
        # self.assertEqual(404, response.status_code)
        self.assertRedirects(
            response, reverse('home'))


class ParticipantDetailViewTest(BaseTestCase):

    def setUp(self):
        super(ParticipantDetailViewTest, self).setUp()
        self.user2 = self.create_user()
        self.url = self.user2.get_absolute_url()

    def test_get(self):
        response = self.client.get(self.url)
        self.assertTrue(self.user.is_authenticated())
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(
            response, 'participants/participant_detail.jade')
        self.assertEqual(self.user2, response.context['participant'])


class ParticipantAdminUserUpdateTest(BaseTestCase):

    def setUp(self):
        super(ParticipantAdminUserUpdateTest, self).setUp()
        self.user2 = self.create_user()
        self.url = reverse(
            'participant_user_update',
            kwargs={
                'pk': self.user2.pk
            }
        )

    def test_get(self):
        response = self.client.get(self.url)
        self.assertTrue(self.user.is_authenticated())
        self.assertEqual(302, response.status_code)
        self.assertEqual(
            response.url, 'http://testserver/admin/login/?next=' + self.url)

    def test_get_user_admin(self):
        self.user.is_staff = True
        self.user.save()

        response = self.client.get(self.url)
        self.assertTrue(self.user.is_authenticated())
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(
            response, 'participants/admin_user_update.jade')
        self.assertIsInstance(response.context['form'], UserForm)
        self.assertEqual(
            response.context['form'].initial['first_name'],
            self.user2.first_name)
        self.assertEqual(
            response.context['form'].initial['last_name'],
            self.user2.last_name)
        self.assertEqual(
            response.context['form'].initial['charge'],
            self.user2.charge)
        self.assertEqual(
            response.context['form'].initial['phone'],
            self.user2.phone)
        self.assertEqual(
            response.context['form'].initial['institution'],
            self.user2.institution)


class UserAdminListViewTest(BaseTestCase):

    def setUp(self):
        super(UserAdminListViewTest, self).setUp()
        self.user2 = self.create_user()
        self.user3 = self.create_user()
        self.user4 = self.create_user()
        self.url = reverse('user_admin_list_view')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertTrue(self.user.is_authenticated())
        self.assertEqual(302, response.status_code)
        self.assertEqual(
            response.url, 'http://testserver/admin/login/?next=' + self.url)

    def test_get_user_admin(self):
        self.user.is_staff = True
        self.user.is_active = True
        self.user.save()

        self.user2.is_staff = False
        self.user2.is_active = True
        self.user2.save()

        self.user3.is_staff = True
        self.user3.is_active = False
        self.user3.save()

        self.user4.is_staff = True
        self.user4.is_superuser = True
        self.user4.save()

        response = self.client.get(self.url)
        self.assertTrue(self.user.is_authenticated())
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(
            response, 'participants/admin_user_list.jade')

        self.assertIn(self.user, response.context['user_list'])
        self.assertNotIn(self.user3, response.context['user_list'])
        self.assertNotIn(self.user3, response.context['user_list'])
        self.assertIn(self.user4, response.context['user_list'])


class AddAdminRedirectViewTest(BaseTestCase):

    def setUp(self):
        super(AddAdminRedirectViewTest, self).setUp()
        self.user2 = self.create_user()
        self.url = reverse(
            'add_admin_redirect', kwargs={'user_pk': self.user2.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertTrue(self.user.is_authenticated())
        self.assertEqual(302, response.status_code)
        self.assertEqual(
            response.url, 'http://testserver/admin/login/?next=' + self.url)

    def test_get_user_admin(self):
        self.user.is_staff = True
        self.user.save()

        self.assertFalse(self.user2.is_staff)
        response = self.client.get(self.url)
        self.assertTrue(self.user.is_authenticated())
        self.assertEqual(302, response.status_code)
        self.assertEqual(
            response.url, 'http://testserver' + reverse('user_admin_list_view')
        )
        self.user2.refresh_from_db()
        self.assertTrue(self.user2.is_staff)


class DeleteAdminRedirectViewTest(BaseTestCase):

    def setUp(self):
        super(DeleteAdminRedirectViewTest, self).setUp()
        self.user2 = self.create_user()
        self.url = reverse(
            'delete_admin_redirect', kwargs={'user_pk': self.user2.pk})

    def test_get(self):
        response = self.client.get(self.url)
        self.assertTrue(self.user.is_authenticated())
        self.assertEqual(302, response.status_code)
        self.assertEqual(
            response.url, 'http://testserver/admin/login/?next=' + self.url)

    def test_get_user_admin(self):
        self.user.is_staff = True
        self.user.save()

        self.user2.is_staff = True
        self.user2.save()

        self.assertTrue(self.user2.is_staff)
        response = self.client.get(self.url)
        self.assertTrue(self.user.is_authenticated())
        self.assertEqual(302, response.status_code)
        self.assertEqual(
            response.url, 'http://testserver' + reverse('user_admin_list_view')
        )
        self.user2.refresh_from_db()
        self.assertFalse(self.user2.is_staff)

    def test_get_same_user_admin(self):
        self.user.is_staff = True
        self.user.save()

        url = reverse(
            'delete_admin_redirect', kwargs={'user_pk': self.user.pk})
        self.assertTrue(self.user.is_staff)
        response = self.client.get(url)
        self.assertTrue(self.user.is_authenticated())
        self.assertEqual(302, response.status_code)
        self.assertEqual(
            response.url, 'http://testserver' + reverse('user_admin_list_view')
        )
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_staff)
