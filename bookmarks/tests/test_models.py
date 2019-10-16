from django.test import TestCase
#from dosgamesfinder.models import Publisher, Genre, DosGame, Screenshot, DownloadLocation
#from django.core.exceptions import ValidationError
#from django.db import IntegrityError, DataError

#User (ID, manyToOne relationships with BookmarksList)
#BookmarksList (Url, manyToOne relationships with links, Privacy flag, pin_code_for_editing)
#Bookmarks (Title, URL, Picture URL)



# Create your tests here.
class BookmarkModelTests(TestCase): 
    def test_create_bookmark(self):
        '''
        Unit Test - User successfully creates a bookmark with a valid title, url and picture
        '''            
        self.fail("finish the test")

    def test_create_bookmark_without_title_throws_validation_error(self):
        '''
        Unit Test - URL and Title are mandatory fields
        '''    
        self.fail("finish the test")

    def test_create_bookmark_without_url_throws_validation_error(self):
        '''
        Unit Test - URL and Title are mandatory fields
        '''        
        self.fail("finish the test")

    def test_create_bookmark_with_faulty_url_throws_validation_error(self):
        '''
        Unit Test - URLs must be valid
        '''        
        self.fail("finish the test")


    def test_create_bookmark_with_image_is_valid(self):
        '''
        Unit Test - pictures must be valid file formats accepted by common browsers
        '''        
        self.fail("finish the test")


    def test_create_bookmark_without_picture(self):
        '''
        Unit Test - Users can create a bookmark without a picture, it should default to a placeholder image
        '''
        self.fail("finish the test")



'''class DosGameModelTests(test_objects_mixin, TestCase): 
    def test_create_dosgame(self):
'''
        ##Unit Test - Ensure that dosgame objects are being saved to the db. 
'''             
        self.assertEquals(self.test_dosgame, DosGame.objects.get(title=self.test_dosgame.title))

    def test_max_length_of_dosgame_title_field(self):
'''
        #Unit Test - This test knows the maximum length of the dosgame title field and tests that assertions are being raised correctly
'''
        # Test the dosgame.title length
        with self.assertRaises(DataError): 
            create_test_dosgame(publisher=self.test_publisher, title=create_breaker_string(513), genre=self.test_genre)

    def test_max_length_of_dosgame_thumbnail_field(self):
        # Test the dosgame.title length
        with self.assertRaises(DataError): 
            create_test_dosgame(publisher=self.test_publisher, title='long thumbnail adventures', thumbnail_src=create_breaker_string(257), genre=self.test_genre)

    def test_default_ordering_of_games(self):
'''
        ##Unit Test - Check that default ordering of all game items is A-Z
'''
        a = create_test_dosgame(publisher=self.test_publisher, genre=self.test_genre, title='a')
        b = create_test_dosgame(publisher=self.test_publisher, genre=self.test_genre, title='b')
        c = create_test_dosgame(publisher=self.test_publisher, genre=self.test_genre, title='c')
        
        test_db_ordering = DosGame.objects.all()
        self.assertEqual([a, b, c, self.test_dosgame], [g for g in test_db_ordering])

    def test_name_method_returns_dosgame_name(self):
'''
        #Unit Test - Ensure that the dosgame returns it's name when calling the models __str__() method
'''
        test_name = 'Adventures in Testingville'
        test_dosgame = create_test_dosgame(publisher=self.test_publisher, genre=self.test_genre, title=test_name)
        self.assertEqual(test_name, test_dosgame.__str__())

    def test_cannot_create_game_without_publisher(self):
'''
        ##Unit Test - Ensure that you aren't able to create game objects without a publisher. 
'''        
        # attempt to create a game without a publisher. Can't use helper function, since that function does it correctly
        test_dosgame = DosGame(
            title="The game with no publisher",
            genre=self.test_genre,
            long_description="This game has no publisher. Was it ever released? Did it even get made? ",
            year_released=1991,
            user_rating=1,
        )

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_dosgame.full_clean()

        with self.assertRaises(IntegrityError): 
            test_dosgame.save()

    def test_cannot_create_game_without_genre(self):
'''
        ##Unit Test - Ensure that you aren't able to create game objects without a genre. 
'''        
        # attempt to create a game without a genre. Can't use helper function, since that function does it correctly
        test_dosgame = DosGame(
            title="The game with no genre",
            long_description="This game has no genre. Is it even a game?",
            year_released=1990,
            user_rating=2,
        )

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_dosgame.full_clean()

        with self.assertRaises(IntegrityError): 
            test_dosgame.save()  

    def test_many_to_one_relationship_between_game_and_screenshot(self):
'''
        ##Unit Test - Create a game, assign it some screenshots, check that the db relationships work as expected. 
'''
        # create two screenshots for the game
        screenshot1 = create_test_screenshot(game=self.test_dosgame)
        screenshot2 = create_test_screenshot(game=self.test_dosgame)

        # and then test
        test_dosgame_db = DosGame.objects.get(title=self.test_dosgame.title)
        test_set_of_screenshots = test_dosgame_db.screenshots.all()
        self.assertEquals([screenshot2, screenshot1], [s for s in test_set_of_screenshots])

    def test_many_to_one_relationship_between_game_and_publisher(self):
'''
        ##Unit Test - Create a publisher, assign it a game, check that the db relationships work as expected. 
'''
        self.assertIn(self.test_dosgame, Publisher.objects.get(name=self.test_publisher.name).dosgame_set.all())     

    def test_many_to_one_relationship_between_game_and_genre(self):
'''
        ##Unit Test - Create a genre, assign it a game, check that the db relationships work as expected. 
'''
        self.assertIn(self.test_dosgame, Genre.objects.get(name=self.test_genre.name).dosgame_set.all())  

    def test_many_to_one_relationship_between_game_and_download_location(self):
'''
        ##Unit Test - Create a game, assign it some download locations, check that the db relationships work as expected. 
'''
        # create two download locations for the game
        download1 = create_test_download_location(game=self.test_dosgame)
        download2 = create_test_download_location(game=self.test_dosgame)

        # and then test
        test_dosgame_db = DosGame.objects.get(title=self.test_dosgame.title)
        test_set_of_download_locations = test_dosgame_db.download_locations.all()
        self.assertEquals([download2, download1], [d for d in test_set_of_download_locations])

    def test_slug_creation(self):
        test_name = 'Make this a slug'
        create_test_dosgame(publisher=self.test_publisher, genre=self.test_genre, title=test_name)
        dosgame_in_db = DosGame.objects.get(title=test_name)
        self.assertEquals(dosgame_in_db.slug, 'make-this-a-slug')

    def test_get_absolute_url(self):
        test_name = 'Make this a url'
        test_dosgame = create_test_dosgame(publisher=self.test_publisher, genre=self.test_genre, title=test_name)
        self.assertEqual(test_dosgame.get_absolute_url(), '/game/make-this-a-url')

    def test_create_model_creates_short_description(self):
        # our long test string is 445 characters in length
        test_description_short = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
        test_description_long = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        
        # truncated string should return at a length no greater than 256 characters, the last 3 characters should be a ..., unless the string is so short that it doesn't need it
        expected_short_description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolo..."

        # first test that a short description isn't truncated and the trailing ... isnt there
        test_dosgame_one = create_test_dosgame(title="tester_one", publisher=self.test_publisher, genre=self.test_genre, long_description=test_description_short)
        self.assertEqual(test_dosgame_one.short_description, test_description_short)
        self.assertNotIn("...", test_dosgame_one.short_description)

        # then test that the longer strings are being truncated properly
        test_dosgame_two = create_test_dosgame(title="tester_two", publisher=self.test_publisher, genre=self.test_genre, long_description=test_description_long)
        self.assertEqual(test_dosgame_two.short_description, expected_short_description)
        self.assertIn("...", test_dosgame_two.short_description)

class ScreenshotModelTests(test_objects_mixin, TestCase):
    def test_create_screenshot(self):
'''
        ##Unit Test - Ensure that screenshot objects are being saved to the db. 
'''             
        test_screenshot = create_test_screenshot(game=self.test_dosgame)
        self.assertEquals([test_screenshot], [s for s in Screenshot.objects.all()])

    def test_max_length_of_screenshot_fields(self):
'''
        ##Unit Test - This test knows the minimum and maximum length of the screenshot fields and tests that assertions are being raised correctly
'''
        # Test the dosgame.title length
        with self.assertRaises(DataError): 
            create_test_screenshot(game=self.test_dosgame, img_src=create_breaker_string(257))

    def test_name_method_returns_screenshot_src(self):
'''
        ##Unit Test - Ensure that the screenshot returns it's src when calling the models __str__() method
'''
        test_img_src = 'https://via.placeholder.com/320x200'
        test_screenshot = create_test_screenshot(game=self.test_dosgame, img_src=test_img_src)
        self.assertEqual(test_img_src, test_screenshot.__str__())

    def test_cannot_create_screenshot_without_game(self):
'''
        ##Unit Test - Ensure that you aren't able to create screenshot objects without games. 
'''
        # attempt to create a screenshot without a game. Can't use helper function, since that function does it correctly
        test_screenshot = Screenshot(
            img_src='https://via.placeholder.com/320x200',
            img_width=320,
            img_height=200,
        )

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_screenshot.full_clean()

        with self.assertRaises(IntegrityError): 
            test_screenshot.save()

class PublisherModelTests(test_objects_mixin, TestCase):
    def test_create_publisher(self):
'''
        ##Unit Test - Ensure that publisher objects are being saved to the db. And that they don't need to be associated with any DosGame objects
'''        
        self.assertIn(self.test_publisher, [p for p in Publisher.objects.all()])
        self.assertEquals(self.test_publisher.name, Publisher.objects.get(name=self.test_publisher.name).name)

    def test_max_length_of_publisher_fields(self):
'''
        ##Unit Test - This test knows the minimum and maximum length of the publisher field and tests that assertions are being raised correctly
'''
        # check that the right assertions are being raised
        with self.assertRaises(DataError): 
            create_test_publisher(name=create_breaker_string(257))

    def test_default_ordering_of_publishers(self):
'''
        ##Unit Test - check that default ordering of all publishers is A-Z
'''
        a = create_test_publisher(name='a')
        b = create_test_publisher(name='b')
        c = create_test_publisher(name='c')
        
        test_db_ordering = Publisher.objects.all()
        self.assertEqual([a, b, c, self.test_publisher], [g for g in test_db_ordering])

    def test_name_method_returns_publisher_name(self):
'''
        ##Unit Test - Ensure that the publisher returns it's name when calling the models name() method
'''
        test_name = 'Test Software Inc'
        test_publisher = create_test_publisher(name=test_name)
        self.assertEqual(test_name, test_publisher.__str__())

    def test_publisher_name_is_unique(self):
'''
        ##Unit Test - Ensure that the publishers name is unique in the database
'''
        # create and save the first publisher
        create_test_publisher(name='test')
        
        # does it raise an Integrity error? 
        with self.assertRaises(IntegrityError): 
            create_test_publisher(name='test')

    def test_get_absolute_url(self):
        test_name = 'Make this a url'
        test_publisher = create_test_publisher(name=test_name)
        self.assertEqual(test_publisher.get_absolute_url(), '/publisher/make-this-a-url')

    def test_games_by_this_publisher(self):
        create_test_dosgame(publisher=self.test_publisher, genre=self.test_genre, title='a')
        create_test_dosgame(publisher=self.test_publisher, genre=self.test_genre, title='b')
        create_test_dosgame(publisher=self.test_publisher, genre=self.test_genre, title='c')
        pub = Publisher.objects.get(name=self.test_publisher.name)
        self.assertEqual(4, pub.games_by_this_publisher()) # 3 + 1 test game that was created in the init method  
        
class GenreModelTests(test_objects_mixin, TestCase):
    def test_create_genre(self):
'''
        #Unit Test - Ensure that genre objects are being saved to the db. And that they don't need to be associated with any DosGame objects
'''        
        self.assertIn(self.test_genre, [g for g in Genre.objects.all()])
        self.assertEquals(self.test_genre.name, Genre.objects.get(name=self.test_genre.name).name)

    def test_max_length_of_genre_fields(self):
'''
        #Unit Test - This test knows the minimum and maximum length of the genre field and tests that assertions are being raised correctly
'''
        # check that the right assertions are being raised
        with self.assertRaises(DataError): 
            create_test_genre(name=create_breaker_string(257))

    def test_default_ordering_of_genres(self):
'''
        #Unit Test - check that default ordering of all genre is A-Z
'''
        a = create_test_genre(name='a')
        b = create_test_genre(name='b') # the self.test_genre's name is 'Adventure', so will fit between a and b 
        c = create_test_genre(name='c')
        
        test_db_ordering = Genre.objects.all()
        self.assertEqual([a, self.test_genre, b, c], [g for g in test_db_ordering])

    def test_name_method_returns_genre_name(self):
'''
        #Unit Test - Ensure that the genre returns it's name when calling the models name() method
'''
        test_name = 'Test Software Inc'
        test_genre = create_test_genre(name=test_name)
        self.assertEqual(test_name, test_genre.__str__())

    def test_genre_is_unique(self):
'''
        #Unit Test - Ensure that the genre name is unique in the database
'''
        # create and save the first publisher
        create_test_genre(name='test')
        
        # does it raise an Integrity error? 
        with self.assertRaises(IntegrityError): 
            create_test_genre(name='test') 

    def test_get_absolute_url(self):
        test_name = 'Make this a url'
        test_genre = create_test_genre(name=test_name)
        self.assertEqual(test_genre.get_absolute_url(), '/genre/make-this-a-url')    

    def test_games_in_this_genre(self):
        create_test_dosgame(publisher=self.test_publisher, genre=self.test_genre, title='a')
        create_test_dosgame(publisher=self.test_publisher, genre=self.test_genre, title='b')
        create_test_dosgame(publisher=self.test_publisher, genre=self.test_genre, title='c')
        g = Genre.objects.get(name=self.test_genre.name)
        self.assertEqual(4, g.games_in_this_genre()) # 3 + 1 test game that was created in the init method         

class DownloadLocationModelTests(test_objects_mixin, TestCase):
    def test_create_download_location(self):
'''
        #Unit Test - Ensure that download location objects are being saved to the db. 
'''             
        test_download_location = create_test_download_location(game=self.test_dosgame)
        self.assertEquals([test_download_location], [s for s in DownloadLocation.objects.all()])

    def test_max_length_of_download_location_href(self):
'''
        #Unit Test - This test knows the minimum and maximum length of the screenshot fields and tests that assertions are being raised correctly
'''
        # Test the dosgame.title length
        with self.assertRaises(DataError): 
            create_test_download_location(game=self.test_dosgame, href=create_breaker_string(257))
    
    def test_default_ordering_of_download_locations(self):
'''
        #Unit Test - Check that default ordering of all download locations is A-Z
'''
        a = create_test_download_location(game=self.test_dosgame, name='a')
        b = create_test_download_location(game=self.test_dosgame, name='b')
        c = create_test_download_location(game=self.test_dosgame, name='c')
        
        test_db_ordering = DownloadLocation.objects.all()
        self.assertEqual([a, b, c], [d for d in test_db_ordering])

    def test_name_method_returns_download_location_name(self):
'''
        #Unit Test - Ensure that the download location returns it's src when calling the models __str__() method
'''
        test_download_location_name = 'GOG'
        test_download_location = create_test_download_location(game=self.test_dosgame, name=test_download_location_name)
        self.assertEqual(test_download_location_name, test_download_location.__str__())

    def test_cannot_create_download_location_without_game(self):
'''
        #Unit Test - Ensure that you aren't able to create download location objects without a game. 
'''
        # attempt to create a download location without a game. Can't use helper function, since that function does it correctly
        test_download_location = DownloadLocation(
            href="www.google.com",
            name="GOG"
        )

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_download_location.full_clean()

        with self.assertRaises(IntegrityError): 
            test_download_location.save() '''