from django.test import TestCase
from .base import test_objects_mixin

class DRFSerailizerTests(test_objects_mixin, TestCase): 
    def test_api_view_not_publicly_accessible(self):
        self.fail('finish the test')

    def test_ListSerializer_returns_data(self):
        url_id = self.test_bookmarks_list.url_id

        response = self.client.get(f'http://localhost:8000/api/Lists/{url_id}/', content_type='json')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['title'], 'My Test Bookmarks')
        self.assertEqual(response.data['url_id'], url_id)

    def test_ListSerializer_returns_bookmark_list(self):
        self.fail('finish the test')

    def test_ListSerializer_excludes_owner(self):
        self.fail('finish the test')

    def test_BookmarkSerializer_excludes_list_foreign_key(self):
        self.fail('finish the test')

