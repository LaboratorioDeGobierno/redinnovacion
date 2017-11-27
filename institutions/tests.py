from django.core.urlresolvers import reverse
from django.utils.text import slugify

from base.tests import BaseTestCase

from .forms import InstitutionForm
from users.models import User


class InstitutionListViewTest(BaseTestCase):

    def setUp(self):
        super(InstitutionListViewTest, self).setUp()
        self.institution = self.create_institution()
        self.url = reverse('institution_list')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(self.user.is_authenticated(), True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(
            response,
            'institutions/most_active_institutions.jade')
        self.assertNotIn(self.institution, response.context['object_list'])

        self.create_user(institution=self.institution)
        response = self.client.get(self.url)
        self.assertIn(self.institution, response.context['object_list'])

    def test_get_user_admin(self):
        self.user.is_staff = True
        self.user.save()

        response = self.client.get(self.url)
        self.assertEqual(self.user.is_authenticated(), True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(
            response,
            'institutions/most_active_institutions.jade')


class InstitutionUserDetailViewTest(BaseTestCase):

    def setUp(self):
        super(InstitutionUserDetailViewTest, self).setUp()
        self.institution = self.create_institution()
        self.url = reverse(
            'institution_detail',
            kwargs={
                'slug': slugify(self.institution.name),
            }
        )

    def test_absolute_url(self):
        self.assertEqual(
            self.url,
            self.institution.get_absolute_url())

    def test_get(self):
        self.user.institution = self.institution
        self.user.status = User.STATUS_ACCEPTED
        self.user.save()
        self.user2 = self.create_user()

        response = self.client.get(self.url)
        self.assertEqual(self.user.is_authenticated(), True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(
            response,
            'institutions/institution_detail.jade')
        self.assertEqual(
            self.institution, response.context['institution'])
        self.assertIn(
            self.user, response.context['user_list'])
        self.assertNotIn(
            self.user2, response.context['user_list'])


class InstitutionUpdateViewTest(BaseTestCase):

    def setUp(self):
        super(InstitutionUpdateViewTest, self).setUp()
        self.institution = self.create_institution()
        self.url = reverse(
            'institution_update',
            kwargs={'slug': slugify(self.institution.name)},
        )

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(self.user.is_authenticated(), True)
        self.assertEqual(302, response.status_code)

    def test_get_is_staff(self):
        self.user.is_staff = True
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(
            response,
            'institutions/institution_update.jade')
        self.assertIsInstance(
            response.context['form'],
            InstitutionForm)


class InstitutionDeleteViewTest(BaseTestCase):

    def setUp(self):
        super(InstitutionDeleteViewTest, self).setUp()
        self.institution = self.create_institution()
        self.url = reverse(
            'institution_delete',
            kwargs={'slug': slugify(self.institution.name)},
        )

    def test_get(self):
        self.user.is_staff = False
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(self.user.is_authenticated(), True)
        self.assertEqual(302, response.status_code)
        self.assertEqual(
            response.url,
            'http://testserver/admin/login/?next=' + self.url
        )

    def test_get_is_staff(self):
        self.user.is_staff = True
        self.user.save()
        self.assertTrue(self.institution.is_active)
        response = self.client.get(self.url)
        self.assertEqual(302, response.status_code)
        self.assertEqual(
            response.url,
            'http://testserver' + reverse('institution_list')
        )
        self.institution.refresh_from_db()
        self.assertFalse(self.institution.is_active)
