from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

MAX_WAIT = 10 # 10 second max wait

class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(MAX_WAIT)
        self.browser.set_page_load_timeout(MAX_WAIT)

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # user visits the home page
        self.browser.get(self.live_server_url)

        self.fail("finish the test")

        # user notices something about the home page.
        #game_cards_row = self.browser.find_element_by_class_name('games-list-row')
        #self.assertEqual(3, len(game_cards_row.find_elements_by_class_name('game-listview')))

class HomePageTests(FunctionalTest):
    def test_something(self):
        self.fail("finish the test")
