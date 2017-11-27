from base.tests import BaseTestCase
from django.core.urlresolvers import reverse


class DocumentationTest(BaseTestCase):
    """
    Base Documentation tests
    """
    def get_object(self):
        self.object = None

    def setUp(self):
        super(DocumentationTest, self).setUp()
        self.get_object()

    def set_superuser(self):
        """
        Set user as superuser
        """
        self.user.is_superuser = True
        self.user.save()

    def access_view(self, type_view, with_args=True, response_status=200):
        """
        Generic test for CRUD
        """
        if self.object:
            _url = "{}_{}".format(
                self.object.__class__.__name__.lower(),
                type_view
            )
            if with_args:
                url = reverse(_url, args=[self.object.id, ])
            else:
                url = reverse(_url)
            response = self.client.get(url)
            self.assertEqual(self.user.is_authenticated(), True)
            self.assertEqual(response_status, response.status_code)

    def test_access_detail_view(self):
        self.access_view(
            'detail',
            with_args=True,
            response_status=200
        )

    def test_access_detail_with_permission(self):
        self.set_superuser()
        self.access_view(
            'detail',
            with_args=True,
            response_status=200
        )

    def test_access_create_view(self):
        self.access_view(
            'create',
            with_args=False,
            response_status=403
        )

    def test_access_create_with_permission(self):
        self.set_superuser()
        self.access_view(
            'create',
            with_args=False,
            response_status=200
        )

    def test_access_update_view(self):
        self.access_view(
            'update',
            with_args=True,
            response_status=403
        )

    def test_access_update_with_permission(self):
        self.set_superuser()
        self.access_view(
            'update',
            with_args=True,
            response_status=200
        )

    def test_access_delete_view(self):
        self.access_view(
            'delete',
            with_args=True,
            response_status=403
        )

    def test_access_delete_with_permission(self):
        self.set_superuser()
        self.access_view(
            'delete',
            with_args=True,
            response_status=200
        )


class MethodologyTest(DocumentationTest):
    def get_object(self):
        self.object = self.create_methodology()


class ToolTest(DocumentationTest):
    def get_object(self):
        self.object = self.create_tool()


class PublicationTest(DocumentationTest):
    def get_object(self):
        self.object = self.create_publication()
