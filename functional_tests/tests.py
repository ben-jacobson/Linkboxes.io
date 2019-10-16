from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from dosgamesfinder.tests.base import create_test_publisher, create_test_genre, create_test_dosgame, create_test_screenshot, create_test_download_location
#from selenium.webdriver.common.keys import Keys
#from time import sleep

MAX_WAIT = 10 # 10 second max wait

class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(MAX_WAIT)
        self.browser.set_page_load_timeout(MAX_WAIT)

        # create 2 test genres
        self.test_action_genre = create_test_genre(name='Action')
        self.test_adventure_genre = create_test_genre(name='Adventure')

        # create 2 test publishers
        self.test_publisher_test_soft = create_test_publisher(name='Test Soft Inc')
        self.test_publisher_foobar_games = create_test_publisher(name='Foo Bar Entertainment')
              
        # create 6 specific test dosgames.
        self.test_dosgame_a = create_test_dosgame(title='Abracadabra', publisher=self.test_publisher_test_soft, genre=self.test_action_genre)
        self.test_dosgame_b = create_test_dosgame(title='Beetlejuice', publisher=self.test_publisher_test_soft, genre=self.test_action_genre)
        self.test_dosgame_c = create_test_dosgame(title='Commandant Ki', publisher=self.test_publisher_test_soft, genre=self.test_adventure_genre)
        self.test_dosgame_d = create_test_dosgame(title='Dodecahedron', publisher=self.test_publisher_foobar_games, genre=self.test_adventure_genre)
        self.test_dosgame_e = create_test_dosgame(title='Explorer Dora', publisher=self.test_publisher_foobar_games, genre=self.test_action_genre)
        self.test_dosgame_f = create_test_dosgame(title='Fortune Finder', publisher=self.test_publisher_foobar_games, genre=self.test_action_genre)

        # to test pagination, we'll create a bunch of dummy anonoymous test games too. So as to keep our filtering tests clean, we'll create separate genre and publisher too.
        self.test_publisher_throwaway_soft = create_test_publisher('Throwaway Games')
        self.test_shovelware_genre = create_test_genre('Shovelware')

        for c in 'abcdefghijklmnopqrstuvwxyz1234567890': # Note that there are separate unit tests for testing the code that enables/disables pagination
            create_test_dosgame(title=c, genre=self.test_shovelware_genre, publisher=self.test_publisher_throwaway_soft)

        # create a test screenshot for each game
        self.test_screenshot_a = create_test_screenshot(game=self.test_dosgame_a)
        self.test_screenshot_b = create_test_screenshot(game=self.test_dosgame_b)
        self.test_screenshot_c = create_test_screenshot(game=self.test_dosgame_c)
        self.test_screenshot_d = create_test_screenshot(game=self.test_dosgame_d)
        self.test_screenshot_e = create_test_screenshot(game=self.test_dosgame_e)
        self.test_screenshot_f = create_test_screenshot(game=self.test_dosgame_f)

        # create a test download location for each game
        self.test_download_location_a = create_test_download_location(game=self.test_dosgame_a)
        self.test_download_location_b = create_test_download_location(game=self.test_dosgame_b)
        self.test_download_location_c = create_test_download_location(game=self.test_dosgame_c)        
        self.test_download_location_d = create_test_download_location(game=self.test_dosgame_d)
        self.test_download_location_e = create_test_download_location(game=self.test_dosgame_e)
        self.test_download_location_f = create_test_download_location(game=self.test_dosgame_f)

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # user visits the home page
        self.browser.get(self.live_server_url)

        # user notices that there are rows of game cards, 3 columns to the row
        game_cards_row = self.browser.find_element_by_class_name('games-list-row')
        self.assertEqual(3, len(game_cards_row.find_elements_by_class_name('game-listview')))

class HomePageTests(FunctionalTest):
    def test_visit_home_page_and_test_search_feature(self):
        # user visits home page and attempts to use the search field. 
        self.browser.get(self.live_server_url)
        search_bar = self.browser.find_element_by_id('search-bar')
        
        # user types something into the search bar. and clicks the search bar. 
        search_bar.send_keys('abracadabra')
        self.browser.find_element_by_id('search-button').click()

        # user is redirected to a new page, user notices url has a search query in it and 'search results for' in the page header
        self.assertIn('search', self.browser.current_url)
        self.assertIn('Search results for', self.browser.find_element_by_tag_name('h1').text)

        # user searched for 'abracadabra', which is test_dosgame_a, user is given exactly one result, that game.
        self.assertEqual(1, len(self.browser.find_elements_by_class_name('game-listview'))) 
        self.assertEqual(self.test_dosgame_a.title, self.browser.find_element_by_link_text(self.test_dosgame_a.title).text)
        
    def test_visit_home_page_and_test_genre_dropdown(self):
        # user visits the home page and clicks on the genre drop down menu
        self.browser.get(self.live_server_url)

        genre_dropdown = self.browser.find_element_by_id('GenreNavbarDropdown')
        genre_dropdown.click()

        # user notices that there are only 3 genres, as we have only created 3 in our class constructor
        genre_filter_buttons = self.browser.find_elements_by_class_name('dropdown-item')
        self.assertEqual(3, len(genre_filter_buttons))

        # user clicks on the action filter
        action_filter = str(self.test_action_genre.slug) + '-filter'
        action_filter_button = self.browser.find_element_by_id(action_filter)
        action_filter_button.click()

        # user is redirected to the action filter, user notices that the title has changed to say "Action Games"
        page_title = self.browser.find_element_by_tag_name('h1')
        self.assertEqual('Action Games', page_title.text)

    def test_visit_home_page_and_visit_game_page(self):
        # user visits the home page and sees a few games on the home page
        self.browser.get(self.live_server_url)
        listview_game_title = self.browser.find_element_by_class_name('game-title-link')
        listview_game_title_text = listview_game_title.text
        listview_game_title.click()

        # user notices that they are taken to a detailview for the game, 
        detailview_game_title = self.browser.find_element_by_tag_name('h1')
        self.assertEqual(listview_game_title_text, detailview_game_title.text)        

        # user goes back to the home page, instead of clicking on the page title, he clicks on the image 
        self.browser.get(self.live_server_url)
        listview_game_title = self.browser.find_element_by_class_name('listView-screenshot')
        listview_game_title.click()

        # user notices that they are taken to the same detailview for whatever game they have selected
        self.assertIn('/game/', self.browser.current_url)

    def test_game_card_links_to_genre(self):
        # user visits the home page and sees a few games on the home page
        self.browser.get(self.live_server_url)

        # user sees that the game card has a genre link and clicks it
        listview_game_genre = self.browser.find_element_by_class_name('card-genre').find_element_by_tag_name('a')
        listview_game_genre_name = listview_game_genre.text
        listview_game_genre.click()

        # user is redirected to a page filtering by that genre. User notices that the title now says something like 'action games' or 'adventure games'
        filterview_page_title =  self.browser.find_element_by_tag_name('h1')
        self.assertEqual(str(listview_game_genre_name) + ' Games', filterview_page_title.text)

    def test_game_card_links_to_publisher_filter(self):
        # user visits the home page and sees a few games on the home page
        self.browser.get(self.live_server_url)

        # user sees that the game card has a genre link and clicks it
        listview_game_publisher = self.browser.find_element_by_class_name('card-publisher-and-date').find_element_by_tag_name('a')
        listview_game_publisher_name = listview_game_publisher.text
        listview_game_publisher.click()

        # user is redirected to a page filtering by that genre. User notices that the title now says something like 'action games' or 'adventure games'
        filterview_page_title =  self.browser.find_element_by_tag_name('h1')
        self.assertEqual('Games by ' + str(listview_game_publisher_name), filterview_page_title.text)

    def test_visit_home_page_pagination(self):
        # user visits the home page and sees a few games on the home page
        self.browser.get(self.live_server_url)        
        
        # user notices that there are some page numbers across the top of the page. 
        # user clicks the number 2 and notices that the url changes
        self.browser.find_element_by_link_text('2').click()
        self.assertIn('/?page=2', self.browser.current_url)

        # user then clicks the prev page button and is taken back to page 1
        self.browser.find_element_by_link_text('Prev').click()
        self.assertIn('/?page=1', self.browser.current_url)

        # user then clicks the next page button and is taken back to page 2    
        self.browser.find_element_by_link_text('Next').click()
        self.assertIn('/?page=2', self.browser.current_url)
        
    def test_visit_home_page_and_visit_publisher_page(self):
        # user visits the home page and clicks on the publisher filter button.
        self.browser.get(self.live_server_url)        
        self.browser.find_element_by_link_text('Publishers').click()
        
        # user notices that the url has changed and that the page title is "All Publishers"
        self.assertIn('/publishers', self.browser.current_url)
        self.assertEqual('All Publishers', self.browser.find_element_by_tag_name('h1').text)

        # user notices 3 publishers on the page, 
        self.assertEqual(self.test_publisher_throwaway_soft.name, self.browser.find_element_by_link_text(self.test_publisher_throwaway_soft.name).text)
        self.assertEqual(self.test_publisher_foobar_games.name, self.browser.find_element_by_link_text(self.test_publisher_foobar_games.name).text)
        self.assertEqual(self.test_publisher_test_soft.name, self.browser.find_element_by_link_text(self.test_publisher_test_soft.name).text)

    def test_visit_home_page_and_filter_by_genre(self):
        # user visits the home page and clicks on the genre filter button, selecting the action genre
        self.browser.get(self.live_server_url)        
        self.browser.find_element_by_link_text('Genres').click()
        self.browser.find_element_by_link_text('Action').click()
        
        # user notices that the url has changed and that the page title is "All Publishers"
        self.assertIn('/genre/action', self.browser.current_url)
        self.assertEqual('Action Games', self.browser.find_element_by_tag_name('h1').text)

        # user notices 4 games in the action genre 
        self.assertEqual(self.test_dosgame_a.title, self.browser.find_element_by_link_text(self.test_dosgame_a.title).text)
        self.assertEqual(self.test_dosgame_b.title, self.browser.find_element_by_link_text(self.test_dosgame_b.title).text)
        self.assertEqual(self.test_dosgame_e.title, self.browser.find_element_by_link_text(self.test_dosgame_e.title).text)
        self.assertEqual(self.test_dosgame_f.title, self.browser.find_element_by_link_text(self.test_dosgame_f.title).text)

class GamePageTests(FunctionalTest):
    def test_visit_game_page_and_test_screenshots(self):
        # user visits a game page
        detailview_url = self.live_server_url + '/game/' + self.test_dosgame_a.slug 
        self.browser.get(detailview_url)        

        # user notices that there are screenshots on the page
        screenshots = self.browser.find_elements_by_class_name('detailView-screenshot')
        self.assertGreater(len(screenshots), 0)

    def test_visit_game_page_and_view_download_links(self): 
        # user visits a game page
        detailview_url = self.live_server_url + '/game/' + self.test_dosgame_a.slug 
        self.browser.get(detailview_url)        

        # user notices that there are download locations listed on the page
        download_locations = self.browser.find_elements_by_class_name('download-location')
        self.assertGreater(len(download_locations), 0)

    def test_visit_game_page_all_games_returns_to_homepage(self):
        # user visits a game page
        original_homepage_url = self.live_server_url + '/'
        detailview_url = self.live_server_url + '/game/' + self.test_dosgame_a.slug 
        self.browser.get(detailview_url)    
        
        # user clicks on the 'all games' button to return to the home page. 
        self.browser.find_element_by_link_text('All Games').click()
        self.assertEqual(self.browser.current_url, original_homepage_url)

    def test_visit_game_page_navbar_logo_returns_to_homepage(self):
        # user visits a game page
        original_homepage_url = self.live_server_url + '/'
        detailview_url = self.live_server_url + '/game/' + self.test_dosgame_a.slug 
        self.browser.get(detailview_url)    
        
        # user clicks on the 'all games' button to return to the home page. 
        self.browser.find_element_by_class_name('navbar-brand').click()
        self.assertEqual(self.browser.current_url, original_homepage_url)        

class PublisherPageTests(FunctionalTest):
    def test_visit_publisher_page_and_select_a_publisher_filter(self):
        # user visits the publisher page
        self.browser.get(self.live_server_url + '/publishers/')

        # user selects on of the publishers and follows the link
        self.browser.find_element_by_link_text(self.test_publisher_foobar_games.name).click()

        # user notices that the page title now says something like 'Games by Foo Bar Games'
        page_title = self.browser.find_element_by_tag_name('h1')
        self.assertEqual(page_title.text, 'Games by ' + str(self.test_publisher_foobar_games.name))

        # user sees that all the games that Foo Bar Games has ever developed can be found here. in this case. games d, e and f
        self.assertEqual(self.test_dosgame_d.title, self.browser.find_element_by_link_text(self.test_dosgame_d.title).text)
        self.assertEqual(self.test_dosgame_e.title, self.browser.find_element_by_link_text(self.test_dosgame_e.title).text)
        self.assertEqual(self.test_dosgame_f.title, self.browser.find_element_by_link_text(self.test_dosgame_f.title).text)
