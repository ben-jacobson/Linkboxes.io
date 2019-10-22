from django.test import TestCase
from .base import test_objects_mixin, create_test_bookmark, create_test_bookmarks_list
from django.urls import reverse

class HomePageTest(TestCase):
    def test_uses_home_template(self):
        '''
        Unit Test - Does the home page view use the correct template?
        '''
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

class BookMarkViewTests(test_objects_mixin, TestCase): 
    def test_bookmarks_listview_uses_correct_template(self):
        '''
        Unit Test - Does the listview use the correct template? Also tests the url_id functionality works
        '''
        test_url_slug = self.test_bookmarks_list.url_id
        response = self.client.get(reverse('bookmarks-listview', kwargs={'slug': test_url_slug}))
        self.assertTemplateUsed(response, 'bookmarks_list.html')

    def test_returns_context_data_page_title(self):
        '''
        Unit Test - The view returns some context data, namely the title of the list. Does it return the correct data?
        '''
        test_url_slug = self.test_bookmarks_list.url_id
        test_list_title = self.test_bookmarks_list.title
        response = self.client.get(reverse('bookmarks-listview', kwargs={'slug': test_url_slug}))
        self.assertEqual(response.context['page_title'], test_list_title) # todo, the page title may change later e.g to include branding

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
        
 