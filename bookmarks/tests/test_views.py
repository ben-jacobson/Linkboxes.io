from django.test import TestCase
from .base import test_objects_mixin, create_test_bookmark, create_test_bookmarks_list
from django.urls import reverse
from bookmarks.models import List

from bookmarks.forms import BookmarkEditForm, BookmarkCreateForm, UserSignUpForm, LinkBoardCreateForm, LinkBoardEditForm
from django.contrib.auth.forms import AuthenticationForm

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
        self.assertIsInstance(response.context['form'], AuthenticationForm)  

    def test_login_page_redirects_after_login(self):
        response = self.client.post(reverse('login'), data={'username': self.test_user_name, 'password': self.test_user_pass})
        self.assertRedirects(response, expected_url=reverse('linkboards-listview'))

class LogoutTest(TestCase):
    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, expected_url=reverse('home'))

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
        test_password = 'C0mpl1c8tedpassword1234!'

        # sign up the user
        signup_data = {'first_name': 'Test', 'last_name': 'Testerson', 'username': test_username, 'password1': test_password, 'password2': test_password}
        response = self.client.post(reverse('signup'), data=signup_data)

        # user should redirect to their linkboards page
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

    def test_page_has_create_form(self):
        response = self.client.get(reverse('bookmarks-listview', kwargs={'slug': self.test_bookmarks_list.url_id}))
        self.assertIsInstance(response.context['form'], BookmarkCreateForm)  

    def test_page_has_edit_form(self):
        response = self.client.get(reverse('bookmarks-listview', kwargs={'slug': self.test_bookmarks_list.url_id}))
        self.assertEquals(response.context['edit_bookmark_form'], BookmarkEditForm)     # was assertIsInstance when we used a form object    
        
    def test_page_create_form_populates_initial_value(self):
        response = self.client.get(reverse('bookmarks-listview', kwargs={'slug': self.test_bookmarks_list.url_id}))
        page_form = response.context['form']
        self.assertEquals(self.test_bookmarks_list.url_id, page_form.initial['list_id'])              

class LinkBoardListViewTests(test_objects_mixin, TestCase):
    def test_uses_correct_template(self):
        '''
        Unit Test - Does the listview use the correct template? Also tests the url_id functionality works
        '''
        self.authenticate(username=self.test_user_name, password=self.test_user_pass) # to avoid the page redirecting to login page

        response = self.client.get(reverse('linkboards-listview'))
        self.assertTemplateUsed(response, 'linkboards_list.html')

    def test_post_form_creates_new_linkboard_when_authenticated(self):
        self.authenticate(username=self.test_user_name, password=self.test_user_pass)

        # create some test data
        test_title = 'test via post method 1234'
        test_data = {
            'title': test_title,
        }

        response = self.client.post(
            reverse('linkboards-listview'),
            data = test_data,
            #content_type='application/json' ,
        )

        self.assertRedirects(response, expected_url=reverse('linkboards-listview'))
        self.assertEqual(List.objects.get(title=test_title).title, test_title)
                
    def test_post_form_returns_forbidden_when_not_authenticated(self):
        # create some test data
        test_title = 'test via post method 1234'
        test_data = {
            'title': test_title,
            'owner': self.test_user.id
        }

        response = self.client.post(
            reverse('linkboards-listview'),
            data = test_data,
        )

        # we should be redirected to a login page
        self.assertRedirects(response, expected_url=reverse('login') + '?redirect_to=' + reverse('linkboards-listview'))

        # the list should not be found in the database
        with self.assertRaises(List.DoesNotExist):
            List.objects.get(title=test_title)

    def test_post_form_cannot_create_lists_for_other_users(self):
        self.authenticate(username=self.test_user_name, password=self.test_user_pass) # authenttcate as a differnt user to the one we just created
        another_test_user = User.objects.create_user("Tester McTesterson", "unittestlover53@hotmail.com", "I don't like testing")
        
        # create some test data
        test_title = 'test via post method 1234'
        test_data = {
            'title': test_title,
            'owner': another_test_user.id   # the form_valid method in the linkboard create view will overwrite this 
        }

        response = self.client.post(
            reverse('linkboards-listview'),
            data = test_data,
        )

        # The server will not raise a forbidden, it will create the list for the authenticated user
        self.assertRedirects(response, expected_url=reverse('linkboards-listview'))
        test_list_query = List.objects.get(title=test_title)
        self.assertEqual(test_list_query.title, test_title)
        self.assertEqual(test_list_query.owner, self.test_user)

    def test_get_returns_only_linkboards_from_authenticated_user(self):
        '''
        Unit Test - When a user is authenticated, sending a GET request to the linkboards page should only return a set of linkboards belonging to that user
        '''        
        second_test_user = User.objects.create_user("Invalid User", "InvalidUser@gotmail.com", "IamInvalid")

        test_list_one = self.test_bookmarks_list # belongs to the authenitcated user
        create_test_bookmarks_list(second_test_user, title="Should not appear") # belongs to a different user

        self.authenticate(username=self.test_user_name, password=self.test_user_pass)
        response = self.client.get(reverse('linkboards-listview'))
        query_set = response.context['linkboards']

        self.assertEqual(len(query_set), 1)
        self.assertEqual(test_list_one.title, query_set[0].title) # there should only be one result

    def test_get_redirects_to_login_page_when_not_authenticated(self):
        '''
        Unit Test - When a user is not authenticated, sending a GET request to the linkboards page should redirect the user to a loging page
        '''        
        response = self.client.get(reverse('linkboards-listview'))
        self.assertRedirects(response, expected_url=reverse('login') + '?redirect_to=' + reverse('linkboards-listview'))

    def test_page_has_create_form(self):
        '''
        Unit Test - The page should have two forms, test that the create form is present
        ''' 
        self.authenticate(username=self.test_user_name, password=self.test_user_pass)
        response = self.client.get(reverse('linkboards-listview'))
        self.assertIsInstance(response.context['form'], LinkBoardCreateForm)  

    def test_page_has_edit_form(self):
        '''
        Unit Test - The page should have two forms, test that the edit form is present
        '''                
        self.authenticate(username=self.test_user_name, password=self.test_user_pass)
        response = self.client.get(reverse('linkboards-listview'))
        self.assertEquals(response.context['edit_linkboard_form'], LinkBoardEditForm) 

        