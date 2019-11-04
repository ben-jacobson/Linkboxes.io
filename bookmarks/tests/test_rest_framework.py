from django.test import TestCase
from .base import test_objects_mixin, create_test_bookmark

class DRFSerailizerTests(test_objects_mixin, TestCase): 
    def test_api_view_not_publicly_accessible(self):
        response = self.client.get(f'/api/', content_type='application/json')
        self.assertNotEqual(response.status_code, 200, msg='browsable api view is available to the public')

    def test_api_view_does_not_allow_list(self):
        '''
        Unit Test- when visiting /api/Lists, it should not allow you to view a list of all bookmarks
        '''
        response = self.client.get(f'/api/Lists/', content_type='application/json')
        self.assertNotEqual(response.status_code, 200, msg="api allows a list view")

    def test_ListSerializer_requires_authentication(self):
        url_id = self.test_bookmarks_list.url_id

        response = self.client.get(f'/api/Lists/{url_id}/', content_type='application/json')
        self.assertNotEqual(response.status_code, 200, msg="api doesn't require any authetication to access")

    def test_ListSerializer_returns_data(self):
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

    def test_BookmarkSerializer_excludes_list_foreign_key(self):
        response = self.client.get(f'/api/Lists/{self.test_bookmarks_list.url_id}/', content_type='application/json')
        self.assertNotIn('_list', response.data['bookmarks'][0])


    def test_can_update_list_with_edit_endpoint(self):
        # capture some of the info up front for comparison
        url_id = self.test_bookmarks_list.url_id
        old_title = self.test_bookmarks_list.title
    
        # update the data with the update endpoint # curl -i -H "Content-Type:application/json" -X PUT http://localhost:8000/api/Lists/g8hjz/ -d '{"title": "The new title1"}'        
        response = self.client.put(
            f'/api/Lists/{url_id}/',
            content_type='application/json',
            data='{"title": "Changed the title to XYZ"}',
        )

        self.assertEquals(response.status_code, 200)
       
        # check that the data has changed
        response = self.client.get(f'/api/Lists/{url_id}/', content_type='application/json')
        self.assertNotEqual(response.data['title'], old_title)
        self.assertEqual(response.data['title'], "Changed the title to XYZ")        

    def test_can_update_bookmark_with_edit_endpoint(self):
        self.fail('finish the test')

    def test_can_only_update_list_with_authenticated_user(self):
        self.fail('finish the test')

    def test_can_only_update_bookmarks_with_authenticated_user(self):
        self.fail('finish the test')
