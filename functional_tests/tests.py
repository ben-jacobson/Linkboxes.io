from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

MAX_WAIT = 10 # 10 second max wait

class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(MAX_WAIT)
        self.browser.set_page_load_timeout(MAX_WAIT)

        # Create 6 test bookmarks,

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # user visits the home page
        self.browser.get(self.live_server_url)

        # user notices the page is live - it shows a set of instructions for how to use the site
        self.assertEqual('Welcome!', self.browser.title)
        self.fail('finish the test')

class BookMarkViewPage(FunctionalTest):
    def test_view_bookmarks_list_view(self):
        # user logs directly into his bookmarks page via it's url. He has remembered his code is abcde
        bookmark_link = 'abcde'
        self.browser.get(self.live_server_url + '/' + bookmark_link)

        # user notices that the page title is what he set it as 'Test List One'
        self.assertEqual('Test List One', self.browser.title)   

        # user notices that there are 6 bookmarks on the page, in a list view
        bookmark_elems = self.browser.find_elements_by_class_name('listView_bookmark')

        # user sees that the first bookmark links to a blog entry that he likes www.google.com
        first_bookmark = bookmark_elems[0]
        self.assertEqual(first_bookmark.text, 'Favourite blog')

        # user clicks one of the links and is taken to that page
        #first_bookmark.click()
        self.assertEqual(self.browser.current_url, 'www.google.com')



        


    
