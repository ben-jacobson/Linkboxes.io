from django.test import TestCase
from .base import test_objects_mixin, create_test_bookmark

class DRFSerailizerTests(test_objects_mixin, TestCase): 
    def test_api_view_not_publicly_accessible(self):
        response = self.client.get(f'/api/', content_type='json')
        self.assertNotEqual(response.status_code, 200, msg='browsable api view is available to the public')

    def test_ListSerializer_returns_data(self):
        url_id = self.test_bookmarks_list.url_id

        response = self.client.get(f'/api/Lists/{url_id}/', content_type='json')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['title'], 'My Test Bookmarks')
        self.assertEqual(response.data['url_id'], url_id)

    def test_ListSerializer_returns_bookmark_list(self):
        create_test_bookmark(self.test_bookmarks_list, title='my other test')

        url_id = self.test_bookmarks_list.url_id
        response = self.client.get(f'/api/Lists/{url_id}/', content_type='json')

        self.assertEqual(len(response.data['bookmarks']), 2)
        self.assertEqual(response.data['bookmarks'][0]['title'], self.test_bookmark.title)
        self.assertEqual(response.data['bookmarks'][1]['title'], 'my other test')
        
    def test_ListSerializer_excludes_owner(self):
        url_id = self.test_bookmarks_list.url_id
        response = self.client.get(f'/api/Lists/{url_id}/', content_type='json')
        self.assertNotIn('owner', response.data)

    def test_BookmarkSerializer_excludes_list_foreign_key(self):
        url_id = self.test_bookmarks_list.url_id
        response = self.client.get(f'/api/Lists/{url_id}/', content_type='json')
        self.assertNotIn('_list', response.data['bookmarks'][0])