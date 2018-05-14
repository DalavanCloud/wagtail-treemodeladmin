from django.test import TestCase

from wagtail.tests.utils import WagtailTestUtils


class TestAuthorIndexView(TestCase, WagtailTestUtils):
    fixtures = ['treemodeladmin_test.json']

    def setUp(self):
        self.user = self.login()

    def get(self, **params):
        return self.client.get('/admin/treemodeladmintest/author/', params)

    def test_author_listing(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['result_count'], 4)
        self.assertContains(response, "Explore J. R. R. Tolkien's books")
        self.assertContains(response, "Add a J. R. Hartley book")

    def test_has_child_admin(self):
        response = self.get()
        self.assertTrue(response.context['view'].has_child_admin)

    def test_breadcrumbs(self):
        resposne = self.get()
        self.assertEqual(
            list(resposne.context['view'].breadcrumbs),
            [('/admin/treemodeladmintest/author/', 'authors')]
        )


class TestBookIndexView(TestCase, WagtailTestUtils):
    fixtures = ['treemodeladmin_test.json']

    def setUp(self):
        self.user = self.login()

    def get(self, **params):
        return self.client.get('/admin/treemodeladmintest/book/', params)

    def test_book_listing(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['result_count'], 4)

    def test_book_listing_filtered(self):
        response = self.get(author=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['result_count'], 2)
        self.assertEqual(
            response.context['view'].get_page_title(),
            'J. R. R. Tolkien'
        )

    def test_has_child_admin(self):
        response = self.get(author=1)
        self.assertFalse(response.context['view'].has_child_admin)

    def test_breadcrumbs(self):
        resposne = self.get(author=1)
        self.assertEqual(
            list(resposne.context['view'].breadcrumbs),
            [
                ('/admin/treemodeladmintest/author/', 'authors'),
                ('/admin/treemodeladmintest/book/', 'books')
            ]
        )