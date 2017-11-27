from base.tests import BaseTestCase


class DynamicContentTest(BaseTestCase):
    """
    Base DynamicContent tests
    """

    def test_replace_order(self):
        parent = self.create_methodology()

        dynamic_content_1 = self.create_dynamic_content(methodology=parent)
        dynamic_content_2 = self.create_dynamic_content(methodology=parent)
        dynamic_content_3 = self.create_dynamic_content(methodology=parent)

        def refresh_from_db():
            dynamic_content_1.refresh_from_db()
            dynamic_content_2.refresh_from_db()
            dynamic_content_3.refresh_from_db()

        self.assertEqual(dynamic_content_1.order, 1)
        self.assertEqual(dynamic_content_2.order, 2)
        self.assertEqual(dynamic_content_3.order, 3)

        # move 3 to the beggining
        dynamic_content_3.replace_order(1)
        refresh_from_db()

        self.assertEqual(dynamic_content_3.order, 1)
        self.assertEqual(dynamic_content_1.order, 2)
        self.assertEqual(dynamic_content_2.order, 3)

        # move 2 to the middle
        dynamic_content_2.replace_order(2)
        refresh_from_db()

        self.assertEqual(dynamic_content_3.order, 1)
        self.assertEqual(dynamic_content_2.order, 2)
        self.assertEqual(dynamic_content_1.order, 3)

        # move 3 to the last
        dynamic_content_3.replace_order(3)
        refresh_from_db()

        self.assertEqual(dynamic_content_2.order, 1)
        self.assertEqual(dynamic_content_1.order, 2)
        self.assertEqual(dynamic_content_3.order, 3)

        # move 2 to the middle
        dynamic_content_2.replace_order(2)
        refresh_from_db()

        self.assertEqual(dynamic_content_1.order, 1)
        self.assertEqual(dynamic_content_2.order, 2)
        self.assertEqual(dynamic_content_3.order, 3)
