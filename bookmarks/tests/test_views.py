from django.test import TestCase
from .base import test_objects_mixin, create_test_bookmark, create_test_bookmarks_list
from django.urls import reverse

from bookmarks.forms import BookmarkEditForm, UserLoginForm, UserSignUpForm
from django.contrib.auth.models import User


class HomePageTest(test_objects_mixin, TestCase):
    def test_uses_correct_template(self):
        '''
        Unit Test - Does the home page view use the correct template?
        '''
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

class LoginTest(test_objects_mixin, TestCase):
    def test_uses_correct_template(self):
        '''
        Unit Test - Does the login view use the correct template?
        '''
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_page_uses_item_form(self):
        response = self.client.get(reverse('login'))
        self.assertIsInstance(response.context['form'], UserLoginForm)  

class SignUpTest(test_objects_mixin, TestCase):
    def test_uses_correct_template(self):
        '''
        Unit Test - Does the login view use the correct template?
        '''
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_page_uses_item_form(self):
        response = self.client.get(reverse('signup'))
        self.assertIsInstance(response.context['form'], UserSignUpForm) 
    
    def test_signup_creates_new_users(self):
        test_username = 'test@test.com'
        test_password = 'testing123'

        # sign up the user
        signup_data = {'first_name': 'Test', 'last_name': 'Testerson', 'username': test_username, 'password': test_password, 'verify_password': test_password}
        response = self.client.post(reverse('signup'), data=signup_data)
        self.assertRedirects(response, expected_url=reverse('linkboards-listview'))

        # test looking up that user in the DB
        test_user_lookup = User.objects.get(username=test_username)
        self.assertEqual(test_user_lookup.username, test_username)


class BookmarkListViewTests(test_objects_mixin, TestCase): 
    def test_uses_correct_template(self):
        '''
        Unit Test - Does the listview use the correct template? Also tests the url_id functionality works
        '''
        test_url_slug = self.test_bookmarks_list.url_id
        response = self.client.get(reverse('bookmarks-listview', kwargs={'slug': test_url_slug}))
        self.assertTemplateUsed(response, 'bookmarks_list.html')

    def test_returns_context_data_page_title(self):
        '''
        Unit Test - The view returns some context data, including the title of the list. Does it return the correct data?
        '''
        test_url_slug = self.test_bookmarks_list.url_id
        test_list_title = self.test_bookmarks_list.title
        response = self.client.get(reverse('bookmarks-listview', kwargs={'slug': test_url_slug}))
        self.assertEqual(response.context['list_name'], test_list_title) # todo, the page title may change later e.g to include branding

    def test_returns_context_data_page_slug(self):
        '''
        Unit Test - The view returns some context data, including the slug of the list. Does it return the correct data?
        '''
        test_url_slug = self.test_bookmarks_list.url_id
        response = self.client.get(reverse('bookmarks-listview', kwargs={'slug': test_url_slug}))
        self.assertEqual(response.context['list_slug'], test_url_slug)


    def test_slug_returns_valid_context(self):
        '''
        Unit Test - if we enter a known slug, will it return only those bookmarks and nothing else? Also tests that the correct context_object_name is set. 
        '''

        # create some test bookmarks we don't expecte to see in the response
        invalid_list = create_test_bookmarks_list(self.test_user, title='We dont want to see bookmarks from this list')
        invalid_link_one = create_test_bookmark(invalid_list, 'invalid link 1')
        invalid_link_two = create_test_bookmark(invalid_list, 'invalid link 2')

        # create some test bookmarks that we expect to see in the response
        how_many_bookmarks_to_test = 10
        test_bookmarks = []

        for i in range(how_many_bookmarks_to_test):
            test_bookmarks.append(create_test_bookmark(self.test_bookmarks_list, title=i))

        # get a response from the server
        test_url_slug = self.test_bookmarks_list.url_id
        response = self.client.get(reverse('bookmarks-listview', kwargs={'slug': test_url_slug}))

        for i in range(how_many_bookmarks_to_test):
            self.assertContains(response, test_bookmarks[i].title)

        self.assertNotContains(response, invalid_link_one.title)
        self.assertNotContains(response, invalid_link_two.title)

    def test_page_uses_item_form(self):
        response = self.client.get(reverse('bookmarks-listview', kwargs={'slug': self.test_bookmarks_list.url_id}))
        self.assertIsInstance(response.context['form'], BookmarkEditForm)        
        
class LinkBoardViewTests(test_objects_mixin, TestCase):
    def test_uses_correct_template(self):
        '''
        Unit Test - Does the listview use the correct template? Also tests the url_id functionality works
        '''
        response = self.client.get(reverse('linkboards-listview'))
        self.assertTemplateUsed(response, 'linkboards_list.html')

    def test_returns_query_set_when_logged_in(self):
        '''
        Unit Test - The view returns some context data, including the title of the list. Does it return the correct data?
        '''
        self.authenticate(username=self.test_user_name, password=self.test_user_pass)
        test_list_title = self.test_bookmarks_list.title
        response = self.client.get(reverse('linkboards-listview'))
        query_set = response.context['linkboards']
        self.assertEqual(test_list_title, query_set[0].title)

    def test_returns_no_data_when_not_logged_in(self):
        '''
        Unit Test - The view returns some context data, including the title of the list. Does it return the correct data?
        '''
        response = self.client.get(reverse('linkboards-listview'))
        query_set = response.context['linkboards']
        self.assertEqual(len(query_set), 0)        