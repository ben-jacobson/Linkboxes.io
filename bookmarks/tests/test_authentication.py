from django.test import TestCase
from .base import test_objects_mixin
from django.contrib.auth.models import User

class ListAuthenticationTests(test_objects_mixin, TestCase):
    def test_authenticate_method(self):
        '''
        Unit Test - test that we can authenticate using the method we created
        '''
        logged_in = self.authenticate(username=self.test_user_name, password=self.test_user_pass)
        self.assertTrue(logged_in)

    def test_ListSerializer_returns_data_with_authentication(self):
        '''
        Unit Test - Test that you can still view data when authenticated
        '''
        self.authenticate(username=self.test_user_name, password=self.test_user_pass)
        url_id = self.test_bookmarks_list.url_id
        response = self.client.get(f'/api/Lists/{url_id}/', content_type='application/json')
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['url_id'], url_id)

    def test_can_update_list_via_put_request_with_authenticated_user(self):
        '''
        Unit Test - test that you can update your own list when you are logged in
        '''
        self.authenticate(username=self.test_user_name, password=self.test_user_pass)

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

    def test_can_not_update_list_without_authenticated_user(self):    
        '''
        Unit Test - test that you cannot update any lists if you aren't logged in, even if you own them
        '''
        # attempt to update the data with the update endpoint # curl -i -H "Content-Type:application/json" -X PUT http://localhost:8000/api/Lists/g8hjz/ -d '{"title": "The new title1"}'        
        response = self.client.put(
            f'/api/Lists/{self.test_bookmarks_list.url_id}/',
            content_type='application/json',
            data='{"title": "Changed the title to XYZ"}',
        )

        # since we didn't authenticate, check that the response is denied
        self.assertEquals(response.status_code, 403)
       
    def test_can_only_update_owned_list(self):
        '''
        Unit Test - test that you can only update lists that you own when logged in
        '''
        # create another user and authenticate as them
        second_test_user_name = 'JimboJones'
        second_test_user_pass = 'oopsmyshirtfelloff'
        User.objects.create_user(second_test_user_name, 'badboy@springfield.com', second_test_user_pass)
        self.authenticate(username=second_test_user_name, password=second_test_user_pass) # authenticate as the first users

        # attempt to update the data of another user. The test_bookmarks list is not owned by them. 
        response = self.client.put(
            f'/api/Lists/{self.test_bookmarks_list.url_id}/',
            content_type='application/json',
            data='{"title": "Changed the title to XYZ"}',
        )

        # Should deny the response response is denied
        self.assertEquals(response.status_code, 403)


class BookmarkAuthenticationTests(test_objects_mixin, TestCase):
    def test_BookmarkSerializer_403s_without_authentication(self):
        '''
        Unit Test - without authentication, the api view should 403
        '''
        bookmark_id = self.test_bookmark.id
        response = self.client.get(f'/api/Bookmark/{bookmark_id}/', content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_BookmarkSerializer_returns_read_only_data_if_authenticated(self):
        '''
        Unit Test - with authentication, user can view their own data
        '''
        # authenticate()
        bookmark_id = self.test_bookmark.id
        response = self.client.get(f'/api/Bookmark/{bookmark_id}/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.test_bookmark.id)
        
    def test_BookmarkSerializer_403s_when_attempting_to_view_other_data(self):
        # authenticate()
        self.fail('finish the test')

    def test_can_update_bookmark_via_put_request_with_authenticated_user(self):
        '''
        Unit Test - test that you can update your own list when you are logged in
        '''
        self.authenticate(username=self.test_user_name, password=self.test_user_pass)

        '''
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
        '''
        self.fail('finish the test')

    def test_cannot_update_bookmark_without_authenticated_user(self):    
        '''
        Unit Test - test that you cannot update any lists if you aren't logged in, even if you own them
        '''
        '''
        # attempt to update the data with the update endpoint # curl -i -H "Content-Type:application/json" -X PUT http://localhost:8000/api/Lists/g8hjz/ -d '{"title": "The new title1"}'        
        response = self.client.put(
            f'/api/Lists/{self.test_bookmarks_list.url_id}/',
            content_type='application/json',
            data='{"title": "Changed the title to XYZ"}',
        )

        # since we didn't authenticate, check that the response is denied
        self.assertEquals(response.status_code, 403)
        '''
        self.fail('finish the test')
       
    def test_can_only_update_owned_list(self):
        '''
        Unit Test - test that you can only update lists that you own when logged in
        '''
        '''
        # create another user and authenticate as them
        second_test_user_name = 'JimboJones'
        second_test_user_pass = 'oopsmyshirtfelloff'
        User.objects.create_user(second_test_user_name, 'badboy@springfield.com', second_test_user_pass)
        self.authenticate(username=second_test_user_name, password=second_test_user_pass) # authenticate as the first users

        # attempt to update the data of another user. The test_bookmarks list is not owned by them. 
        response = self.client.put(
            f'/api/Lists/{self.test_bookmarks_list.url_id}/',
            content_type='application/json',
            data='{"title": "Changed the title to XYZ"}',
        )

        # Should deny the response response is denied
        self.assertEquals(response.status_code, 403)
        '''
        self.fail('finish the test')