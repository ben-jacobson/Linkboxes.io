from django.test import TestCase
from .base import test_objects_mixin, create_test_bookmark

class ListEndpointTests(test_objects_mixin, TestCase): 
    def test_api_view_not_publicly_accessible(self):
        '''
        Unit Test - viewing the api root is not allowed
        '''
        response = self.client.get(f'/api/', content_type='application/json')
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 403)

    def test_api_list_view_is_not_viewable(self):
        '''
        Unit Test - when visiting /api/Lists, it should not allow you to view a list of all Lists
        '''
        response = self.client.get(f'/api/Lists/', content_type='application/json')
        self.assertNotEqual(response.status_code, 200, msg="api allows a list view")

    def test_ListSerializer_returns_readonly_data_without_authentication(self):
        url_id = self.test_bookmarks_list.url_id
        response = self.client.get(f'/api/Lists/{url_id}/', content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['url_id'], url_id)

    def test_ListSerializer_returns_bookmark_list(self):
        create_test_bookmark(self.test_bookmarks_list, title='my other test')

        url_id = self.test_bookmarks_list.url_id
        response = self.client.get(f'/api/Lists/{url_id}/', content_type='application/json')

        self.assertEqual(len(response.data['bookmarks']), 2)
        self.assertEqual(response.data['bookmarks'][0]['title'], self.test_bookmark.title)
        self.assertEqual(response.data['bookmarks'][1]['title'], 'my other test')
        
    def test_ListSerializer_excludes_owner(self):
        url_id = self.test_bookmarks_list.url_id
        response = self.client.get(f'/api/Lists/{url_id}/', content_type='application/json')
        self.assertNotIn('owner', response.data)

    def test_ListSerializer_excludes_id(self):
        url_id = self.test_bookmarks_list.url_id
        response = self.client.get(f'/api/Lists/{url_id}/', content_type='application/json')
        self.assertNotIn('id', response.data)        

    def test_reorder_api_endpoint_when_authenticated(self):
        url_id = self.test_bookmarks_list.url_id
        response = self.client.get(f'/api/Lists/{url_id}/reorder', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_reorder_api_endpoint_when_not_authenticated(self):
        self.fail('finish the test')  

class BookmarkSerializerTests(test_objects_mixin, TestCase): 
    def test_api_list_view_is_not_viewable(self):
        '''
        Unit Test- when visiting /api/Bookmark, it should not allow you to view a list of all Lists
        '''
        response = self.client.get(f'/api/Bookmark/', content_type='application/json')
        self.assertEqual(response.status_code, 404)
        
    def test_ListSerializer_shows_foreign_key(self):
        '''
        Unit Test- when visiting /api/Bookmark, it should not show you the owner
        '''
        self.authenticate(username=self.test_user_name, password=self.test_user_pass)
        response = self.client.get(f'/api/Bookmark/{self.test_bookmark.id}/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('_list', response.data)
