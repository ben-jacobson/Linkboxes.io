from django.test import TestCase
from .base import test_objects_mixin, create_test_bookmarks_list
from django.contrib.auth.models import User
from bookmarks.models import Bookmark, List
from django.urls import reverse

class ListAuthenticationTests(test_objects_mixin, TestCase):
    def test_authenticate_method(self):
        '''
        Unit Test - test that we can authenticate using the method we created
        '''
        logged_in = self.authenticate(username=self.test_user_name, password=self.test_user_pass)
        self.assertTrue(logged_in)

    def test_ListSerializer_returns_data_with_authentication(self):
        '''
        Unit Test - Test that you can view List data when authenticated
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
        Unit Test - test that you can only update lists that you own
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

    def test_list_delete_method_with_authentication(self):
        # The user is logged in
        self.authenticate(username=self.test_user_name, password=self.test_user_pass)
        
        # attempt the DELETE method
        response = self.client.delete(   # will go with patch to avoid updating other fields for now. 
            f'/api/Lists/{self.test_bookmarks_list.url_id}/',
        )

        # did we get the correct status code in return?
        self.assertEquals(response.status_code, 204) # 200 is ideal, but 204 is fine. 

        # now look up the data, there should be zero results for that particular ID
        with self.assertRaises(Bookmark.DoesNotExist):
            Bookmark.objects.get(url=self.test_bookmarks_list.url_id)
        
    def test_list_delete_method_without_authentication(self):
        # The user is not logged in and attempts the DELETE method
        response = self.client.delete(   # will go with patch to avoid updating other fields for now. 
            f'/api/Lists/{self.test_bookmarks_list.url_id}/',
        )

        # did we get the correct status code in return?
        self.assertEquals(response.status_code, 403)  

        # now look up the data, there should still be results for that particular ID
        test_query = List.objects.get(url_id=self.test_bookmarks_list.url_id)
        self.assertEqual(test_query.title, self.test_bookmarks_list.title)        

    def test_can_only_delete_owned_list(self):
        # authenticate as a different user. 
        second_test_user_name = 'JimboJones'
        second_test_user_pass = 'oopsmyshirtfelloff'
        User.objects.create_user(second_test_user_name, 'badboy@springfield.com', second_test_user_pass)
        self.authenticate(username=second_test_user_name, password=second_test_user_pass) # authenticate as the first users

        response = self.client.delete(   # will go with patch to avoid updating other fields for now. 
            f'/api/Lists/{self.test_bookmarks_list.url_id}/',
        )

        # did we get the correct status code in return?
        self.assertEquals(response.status_code, 403)  

        # now look up the data, there should still be results for that particular ID
        test_query = List.objects.get(url_id=self.test_bookmarks_list.url_id)
        self.assertEqual(test_query.title, self.test_bookmarks_list.title)  

class BookmarkAuthenticationTests(test_objects_mixin, TestCase):
    def test_BookmarkSerializer_retrieve_403s_without_authentication(self):
        '''
        Unit Test - without authentication, the api view should 403
        '''
        bookmark_id = self.test_bookmark.id
        response = self.client.get(f'/api/Bookmark/{bookmark_id}/', content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_BookmarkSerializer_retrievess_data_if_authenticated(self):
        '''
        Unit Test - with authentication, user can view their own data
        '''
        self.authenticate(username=self.test_user_name, password=self.test_user_pass)
        bookmark_id = self.test_bookmark.id
        response = self.client.get(f'/api/Bookmark/{bookmark_id}/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.test_bookmark.title)
        
    def test_BookmarkSerializer_403s_when_attempting_to_retrieve_data_owned_by_other_user(self):
        '''
        Unit Test - If authenticated, can we view other people's data?
        '''
        # Create a second user and authenticate
        second_test_user_name = 'JimboJones'
        second_test_user_pass = 'oopsmyshirtfelloff'
        User.objects.create_user(second_test_user_name, 'badboy@springfield.com', second_test_user_pass)
        self.authenticate(username=second_test_user_name, password=second_test_user_pass) # authenticate as the second test user

        # attempt to view the data of another user
        bookmark_id = self.test_bookmark.id
        response = self.client.get(f'/api/Bookmark/{bookmark_id}/', content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_can_update_bookmark_via_put_request_with_authenticated_user(self):
        '''
        Unit Test - test that you can update your own bookmark when you are logged in
        '''
        self.authenticate(username=self.test_user_name, password=self.test_user_pass)

        # capture some of the info up front for comparison
        bookmark_id = self.test_bookmark.id
        old_title = self.test_bookmark.title
    
        # update the data with the update endpoint # curl -i -H "Content-Type:application/json" -X PATCH http://localhost:8000/api/Bookmark/1/ -d '{"title": "The new title1"}'        
        response = self.client.patch(   # will go with patch to avoid updating other fields for now. 
            f'/api/Bookmark/{bookmark_id}/',
            content_type='application/json',
            data='{"title": "Changed the title to XYZ"}',
        )
        self.assertEquals(response.status_code, 200)
       
        # check that the data has changed
        response = self.client.get(f'/api/Bookmark/{bookmark_id}/', content_type='application/json')
        self.assertNotEqual(response.data['title'], old_title)
        self.assertEqual(response.data['title'], "Changed the title to XYZ")        
        
    def test_cannot_update_bookmark_without_authenticated_user(self):    
        '''
        Unit Test - test that you cannot update any lists if you aren't logged in, even if you own them
        '''
        # attempt to update the data with the update endpoint # curl -i -H "Content-Type:application/json" -X PUT http://localhost:8000/api/Lists/g8hjz/ -d '{"title": "The new title1"}'        
        response = self.client.patch(   # will go with patch to avoid updating other fields for now. 
            f'/api/Bookmark/{self.test_bookmark.id}/',
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
        response = self.client.patch(   # will go with patch to avoid updating other fields for now. 
            f'/api/Bookmark/{self.test_bookmark.id}/',
            content_type='application/json',
            data='{"title": "Changed the title to XYZ"}',
        )

        # Should deny the response response is denied
        self.assertEquals(response.status_code, 403)

    def test_bookmark_delete_method_with_authentication(self):
        # The user is logged in
        self.authenticate(username=self.test_user_name, password=self.test_user_pass)
        
        # attempt the DELETE method
        response = self.client.delete(   # will go with patch to avoid updating other fields for now. 
            f'/api/Bookmark/{self.test_bookmark.id}/',
        )

        # did we get the correct status code in return?
        self.assertEquals(response.status_code, 204) # 200 is ideal, but 204 is fine. 

        # now look up the data, there should be zero results for that particular ID
        with self.assertRaises(Bookmark.DoesNotExist):
            Bookmark.objects.get(id=self.test_bookmark.id)
        
    def test_bookmark_delete_method_without_authentication(self):
        # The user is not logged in and attempts the DELETE method
        response = self.client.delete(   # will go with patch to avoid updating other fields for now. 
            f'/api/Bookmark/{self.test_bookmark.id}/',
        )

        # did we get the correct status code in return?
        self.assertEquals(response.status_code, 403)  

        # now look up the data, there should still be results for that particular ID
        test_query = Bookmark.objects.get(id=self.test_bookmark.id)
        self.assertEqual(test_query.title, self.test_bookmark.title)

    def test_can_only_delete_owned_bookmarks(self):
        # authenticate as a different user. 
        second_test_user_name = 'JimboJones'
        second_test_user_pass = 'oopsmyshirtfelloff'
        User.objects.create_user(second_test_user_name, 'badboy@springfield.com', second_test_user_pass)
        self.authenticate(username=second_test_user_name, password=second_test_user_pass) # authenticate as the first users

        response = self.client.delete(   # will go with patch to avoid updating other fields for now. 
            f'/api/Bookmark/{self.test_bookmark.id}/',
        )

        # did we get the correct forbidden status code in return?
        self.assertEquals(response.status_code, 403)  

        # now look up the data, there should still be results for that particular ID
        test_query = Bookmark.objects.get(id=self.test_bookmark.id)
        self.assertEqual(test_query.title, self.test_bookmark.title)        


class CreateNewBookmarkAuthenticationTests(test_objects_mixin, TestCase):
    def test_create_new_bookmark_with_post_method_after_logging_in(self):
        '''
        Unit Test - POSTing to the listview will create another bookmark in that list, but only if you are authenticated as the right user
        '''
        self.authenticate(username=self.test_user_name, password=self.test_user_pass)
        new_bookmark_item_title = 'Hello, this is my new item'
        response = self.client.post(reverse('bookmarks-listview', kwargs={'slug': self.test_bookmarks_list.url_id}), data={'title': new_bookmark_item_title, 'url': 'www.google.com', 'thumbnail_url': 'www.google.com', 'list_id': self.test_bookmarks_list.url_id})
        self.assertRedirects(response, expected_url=reverse('bookmarks-listview', kwargs={'slug': self.test_bookmarks_list.url_id})) # does the page redirect to the correct place?
        self.assertEquals(new_bookmark_item_title, Bookmark.objects.get(title=new_bookmark_item_title).title) # can the object be found in the database? 
        self.assertEquals(self.test_bookmarks_list.owner, Bookmark.objects.get(title=new_bookmark_item_title)._list.owner) # does the owner match? 

    def test_create_new_bookmark_with_post_method_without_logging_in(self):
        '''
        Unit Test - POSTing to the listview of another user will not create another bookmark in the list, because you are not authenticated as them
        '''
        post_data = {'title': 'Hello, this is my new item', 'url': 'www.google.com', 'thumbnail_url': 'www.google.com', 'list_id': self.test_bookmarks_list.url_id}        
        response = self.client.post(reverse('bookmarks-listview', kwargs={'slug': self.test_bookmarks_list.url_id}), data=post_data)
        self.assertEquals(response.status_code, 403) # do we get a forbidden response

    def test_create_new_bookmark_with_injecting_list_not_owned_by_user(self):
        '''
        Unit Test - POSTing to the listview of another user will not create another bookmark in the list, because you are not authenticated as them
        '''
        # create a new user and a new bookmark list to go with it
        new_test_user = User.objects.create_user('imauser@users.com', 'imauser@users.com', 'bestPasswordEva') # create a new user
        new_test_bookmarks_list = create_test_bookmarks_list(new_test_user) # create a test bookmark with the new user

        # authenticate as the old user 
        self.authenticate(username=self.test_user_name, password=self.test_user_pass) 

        # while authenticated as the old user, try to update a bookmark that belongs to the new user by injecting into the post data
        post_data = {'title': 'Hello, this is my new item', 'url': 'www.google.com', 'thumbnail_url': 'www.google.com', 'list_id': new_test_bookmarks_list.url_id} # url_id differs from the page we look up
        response = self.client.post(reverse('bookmarks-listview', kwargs={'slug': self.test_bookmarks_list.url_id}), data=post_data)
        
        # we should get a forbidden response
        self.assertEquals(response.status_code, 403)

    def test_create_new_bookmark_injecting_other_list_owned_by_user(self):
        '''
        Unit Test - Using your browsers development tools, you can insert a different list id into the hidden field of the form, the server should respond with a forbidden code
        '''
        # Create a new list and authenticate as that user
        new_test_bookmarks_list = create_test_bookmarks_list(self.test_user)
        self.authenticate(username=self.test_user_name, password=self.test_user_pass) 

        # the owners are the same
        self.assertEqual(new_test_bookmarks_list.owner, self.test_bookmarks_list.owner)

        # attempt to update lists owned by you, by injecting into the post data
        post_data = {'title': 'Hello, this is my new item', 'url': 'www.google.com', 'thumbnail_url': 'www.google.com', 'list_id': new_test_bookmarks_list.url_id}
        response = self.client.post(reverse('bookmarks-listview', kwargs={'slug': self.test_bookmarks_list.url_id}), data=post_data)
        
        # we should get a forbidden response
        self.assertEquals(response.status_code, 403) # do we get a forbidden response