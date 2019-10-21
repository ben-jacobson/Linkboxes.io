from django.test import TestCase
from django.urls import reverse

class HomePageTest(TestCase):
    def test_uses_home_template(self):
        '''
        Unit Test - Does the home page view use the correct template?
        '''
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

class BookMarkViewTests(TestCase): 
    def test_uses_listview_template(self):
        '''
        Unit Test - Does the listview use the correct template?
        '''
        test_url_slug = 'abcde'
        response = self.client.get(reverse('bookmarks-listview', kwargs={'slug': test_url_slug}))
        self.assertTemplateUsed(response, 'bookmarks_list.html')

    def test_returns_context_data_page_title(self):
        '''
        Unit Test - The view returns some context data, namely the title of the list. Does it return the correct data?
        '''
        self.fail('finish the test')

    def test_slug_returns_valid_context(self):
        '''
        Unit Test - if we enter a known slug, will it return only those bookmarks and nothing else?
        '''
        self.fail('finish the test')