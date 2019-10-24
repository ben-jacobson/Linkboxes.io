from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from django.contrib.auth.models import User
from bookmarks.tests.base import create_test_bookmark, create_test_bookmarks_list

MAX_WAIT = 10 # 10 second max wait

class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(MAX_WAIT)
        self.browser.set_page_load_timeout(MAX_WAIT)

        # set up some DRY variables to use throughout these tests
        self.home_page_main_header = 'INSERT LOGO HERE'
        self.bookmark_list_page_title = 'Saved bookmarks'

        # create our test user, a test bookmarks list
        self.test_user = User.objects.create_user('Joe Bloggs', 'joe@bloggs.com', 'joepassword')
        self.test_list = create_test_bookmarks_list(self.test_user, title=self.bookmark_list_page_title)
        self.test_list_slug = self.test_list.url_id

        # create some test bookmarks
        self.test_bookmarks = []
        self.test_bookmarks.append(create_test_bookmark(self.test_list, title='My favourite blog'))
        self.test_bookmarks.append(create_test_bookmark(self.test_list, title='Chicken Cacciatori Recipe'))
        self.test_bookmarks.append(create_test_bookmark(self.test_list, title='Spiderman Movie Spoiler Alerts'))
        self.test_bookmarks.append(create_test_bookmark(self.test_list, title='Red Socks'))
        self.test_bookmarks.append(create_test_bookmark(self.test_list, title='What species of spider are you?'))
        self.test_bookmarks.append(create_test_bookmark(self.test_list, title='Elsagate: A government conspiracy?'))

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # user visits the home page
        self.browser.get(self.live_server_url)

        # user notices the page is live - it shows a set of instructions for how to use the site
        self.assertEqual('Welcome!', self.browser.title)

        page_h1 = self.browser.find_element_by_id('main-header') # will find the first one on the page
        self.assertEqual(page_h1.text, self.home_page_main_header)

        self.fail('finish the test - put in something to test that the stylesheet was loaded correctly, e.g check that something is centered')

class BookMarkViewPage(FunctionalTest):
    def test_view_bookmarks_list_view_read_only(self):
        # user logs directly into his bookmarks page via it's url. He has remembered his code is abcde
        bookmark_link = self.test_list_slug
        self.browser.get(self.live_server_url + '/' + bookmark_link)

        # user notices the page title 
        self.assertEqual(self.bookmark_list_page_title, self.browser.title)   

        # user notices the header
        page_header = self.browser.find_element_by_tag_name('h1')
        self.assertEqual(self.bookmark_list_page_title, page_header.text)   

        # user notices that there are 6 bookmarks on the page, in a list view
        bookmark_elems = self.browser.find_elements_by_class_name('bookmark-link')
        self.assertEquals(len(bookmark_elems), 6)

        # user sees that the first bookmark links to a blog entry that he likes www.google.com
        first_bookmark = bookmark_elems[0]
        self.assertEqual(first_bookmark.text, 'My favourite blog')

        # user sees that the bookmarks are all hyperlinks
        self.assertEqual(first_bookmark.tag_name, 'a')
        first_bookmark_hyperlink = self.browser.find_elements_by_link_text(first_bookmark.text)
        self.assertEqual(len(first_bookmark_hyperlink), 1)

        # user clicks one of the links and is taken to that page
        first_bookmark.click()
        self.assertIn('www.google.com', self.browser.current_url)

    def test_login_feature_from_home_page(self):
        # user visits home page, notices the login button and clicks it

        # user logs in and sees his list of bookmark lists
        self.fail('finish the test')

    def test_edit_a_bookmarks_list(self):
        # user visits a bookmark list he owns, and clicks edit

        # user is taken to the login screen and logs in

        # user is redirected back to the page he wanted to edit

        # user clicks the pencil icon next to the item he wants to edit

        # user edits the item, saves it and logs out

        # user revisits the page to make sure, lo and behold the edit took place
        self.fail('finish the test')