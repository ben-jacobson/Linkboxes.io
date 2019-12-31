from django.test import TestCase
from .base import test_objects_mixin, create_test_bookmark
from bookmarks.models import Bookmark
from json import dumps

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

    def test_reorder_api_endpoint_get_method(self):
        url_id = self.test_bookmarks_list.url_id
        response = self.client.get(f'/api/Lists/{url_id}/reorder/', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_reorder_api_endpoint_when_not_authenticated(self):
        # run the post method to see how this responds
        url_id = self.test_bookmarks_list.url_id
        test_reorder_data = [1, 2, 3, 4]

        # make the request
        response = self.client.patch(
            f'/api/Lists/{url_id}/reorder/', 
            data={'new_order': test_reorder_data}, 
            content_type='application/json' 
        )

        self.assertEqual(response.status_code, 403) # since we aren't authenticated, it should fail

    def test_reorder_api_endpoint_when_authenticated(self):
        # ensure we are logged in 
        self.authenticate(username=self.test_user_name, password=self.test_user_pass) # this user owns the test_bookmarks_list

        # start by creating some new bookmarks
        new_test_bookmarks = []
        for i in range(10):
            new_test_bookmarks.append(Bookmark(title=f'Bookmark {i+1}', thumbnail_url='www.google.com', url='www.google.com', _list=self.test_bookmarks_list).save())

        # our new order
        new_order = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1] # array of indexes to be changed into a string

        # run the post method to see how this responds
        url_id = self.test_bookmarks_list.url_id
        json_data = dumps({'new_order': new_order})     # should be equivalent to JS JSON.stringify?

        self.client.patch(
            f'/api/Lists/{url_id}/reorder/', 
            data=json_data, 
            content_type='application/json' # this request will not work without this. 
        )

        # sending the request should re-order the bookmarks
        self.assertEqual([i for i in self.test_bookmarks_list.get_bookmark_order()], new_order)

    def test_delete_data_deletes_a_linkboard_when_authenticated(self):
        '''
        Unit Test - When a user is authenticated, sending a DELETE request for a specific linkboards should delete the linkboard
        '''
        self.authenticate(username=self.test_user_name, password=self.test_user_pass) # this user owns the test_bookmarks_list
        url_id = self.test_bookmarks_list.url_id

        # don't authenticate and make the request
        response = self.client.delete(
            f'/api/Lists/{url_id}/', 
            content_type='application/json' 
        )

        self.assertEqual(response.status_code, 204) 

    def test_delete_data_returns_error_when_not_authenticated(self):
        '''
        Unit Test - When no user is authenticated, sending a DELETE request should return 403 Forbidden
        '''   
        url_id = self.test_bookmarks_list.url_id

        # don't authenticate and make the request
        response = self.client.delete(
            f'/api/Lists/{url_id}/', 
            content_type='application/json' 
        )

        self.assertEqual(response.status_code, 403) # since we aren't authenticated, it should fail


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
