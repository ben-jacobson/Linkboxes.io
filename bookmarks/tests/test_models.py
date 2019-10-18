from django.test import TestCase
from .base import test_objects_mixin, create_test_bookmark, create_test_junk_data
from bookmarks.models import Bookmark, BookmarksList

from django.core.exceptions import ValidationError
from django.db import IntegrityError

MAX_TITLE_LEN = 512
MAX_URL_LEN = 2048

class BookmarkModelTests(test_objects_mixin, TestCase): 
    def test_create_bookmark(self):
        '''
        Unit Test - User successfully creates a bookmark with a valid title, url, picture - linked to a valid bookmarks list
        '''   
        self.assertEquals(self.test_bookmark, Bookmark.objects.get(title=self.test_bookmark.title))

    def test_creating_a_bookmark_without_list_throws_validation_error(self):
        test_bookmark = Bookmark(
            title='asdf',
            thumbnail_url='asdf',
            url='asdf',
        )

        with self.assertRaises(IntegrityError):
            test_bookmark.save()


    def test_create_bookmark_without_title_throws_validation_error(self):
        '''
        Unit Test - URL and Title are mandatory fields
        '''    
        test_bookmark_without_title = create_test_bookmark(self.test_bookmarks_list, title='')

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmark_without_title.full_clean()

    def test_create_bookmark_without_url_throws_validation_error(self):
        '''
        Unit Test - URL and Title are mandatory fields
        '''        
        test_bookmark_without_url = create_test_bookmark(self.test_bookmarks_list, url='')

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmark_without_url.full_clean()

    # We had model validation for correct urls and image types, but playing with the model validation proved to be to finnicky. Plus it would mean less flexibility in future migrations. Best that we handle all validation of this data at the form layer. 

    def test_create_bookmark_without_picture(self):
        '''
        Unit Test - Users can create a bookmark without a picture, it should default to a placeholder image
        '''
        test_bookmark_without_image = create_test_bookmark(self.test_bookmarks_list, thumbnail_url='')
        test_bookmark_without_image.save()
        self.assertEqual(test_bookmark_without_image.thumbnail_url, '/no_thumbnail.jpg')

    def test_title_max_length(self):
        test_bookmark_with_long_title = create_test_bookmark(self.test_bookmarks_list, title=create_test_junk_data(MAX_TITLE_LEN + 1))

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmark_with_long_title.full_clean()

    def test_thumbnail_max_length(self):
        test_bookmark_with_long_thumbnail = create_test_bookmark(self.test_bookmarks_list, thumbnail_url=create_test_junk_data(MAX_URL_LEN + 1))

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmark_with_long_thumbnail.full_clean()

    def test_url_max_length(self):
        test_bookmark_with_long_url = create_test_bookmark(self.test_bookmarks_list, url=create_test_junk_data(MAX_URL_LEN + 1))

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmark_with_long_url.full_clean()

class BookmarksListModelTests(test_objects_mixin, TestCase): 
    def test_create_bookmark_list(self):
        '''
        Unit Test - User successfully creates a bookmark list with a valid title, url and picture
        '''   
        self.assertEquals(self.test_bookmarks_list, BookmarksList.objects.get(title=self.test_bookmarks_list.title))

    def test_create_bookmark_without_title_throws_validation_error(self):
        '''
        Unit Test - URL and Title are mandatory fields
        '''    
        test_bookmark_without_title = create_test_bookmark(self.test_bookmarks_list, title='')

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmark_without_title.full_clean()
        self.fail('finish the test')


    def test_create_bookmark_without_url_throws_validation_error(self):
        '''
        Unit Test - URL and Title are mandatory fields
        '''        
        test_bookmark_without_url = create_test_bookmark(self.test_bookmarks_list, url='')

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmark_without_url.full_clean()

        self.fail('finish the test')

    def test_create_bookmark_without_picture(self):
        '''
        Unit Test - Users can create a bookmark without a picture, it should default to a placeholder image
        '''
        test_bookmark_without_image = create_test_bookmark(self.test_bookmarks_list, thumbnail_url='')
        test_bookmark_without_image.save()
        self.assertEqual(test_bookmark_without_image.thumbnail_url, '/no_thumbnail.jpg')
        self.fail('finish the test')

    def test_title_max_length(self):
        test_bookmark_with_long_title = create_test_bookmark(self.test_bookmarks_list, title=create_test_junk_data(MAX_TITLE_LEN + 1))

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmark_with_long_title.full_clean()
        self.fail('finish the test')


    def test_thumbnail_max_length(self):
        test_bookmark_with_long_thumbnail = create_test_bookmark(self.test_bookmarks_list, thumbnail_url=create_test_junk_data(MAX_URL_LEN + 1))

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmark_with_long_thumbnail.full_clean()
        self.fail('finish the test')
            

    def test_url_max_length(self):
        test_bookmark_with_long_url = create_test_bookmark(self.test_bookmarks_list, url=create_test_junk_data(MAX_URL_LEN + 1))

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmark_with_long_url.full_clean()
        self.fail('finish the test')


class UserModelTests(test_objects_mixin, TestCase): 
    def test_create_bookmark(self):
        '''
        Unit Test - User successfully creates a bookmark with a valid title, url and picture
        '''   
        self.assertEquals(self.test_bookmark, Bookmark.objects.get(title=self.test_bookmark.title))
        self.fail('finish the test')

    def test_create_bookmark_without_title_throws_validation_error(self):
        '''
        Unit Test - URL and Title are mandatory fields
        '''    
        test_bookmark_without_title = create_test_bookmark(self.test_bookmarks_list, title='')

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmark_without_title.full_clean()
        self.fail('finish the test')


    def test_create_bookmark_without_url_throws_validation_error(self):
        '''
        Unit Test - URL and Title are mandatory fields
        '''        
        test_bookmark_without_url = create_test_bookmark(self.test_bookmarks_list, url='')

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmark_without_url.full_clean()

        self.fail('finish the test')

    def test_create_bookmark_without_picture(self):
        '''
        Unit Test - Users can create a bookmark without a picture, it should default to a placeholder image
        '''
        test_bookmark_without_image = create_test_bookmark(self.test_bookmarks_list, thumbnail_url='')
        test_bookmark_without_image.save()
        self.assertEqual(test_bookmark_without_image.thumbnail_url, '/no_thumbnail.jpg')
        self.fail('finish the test')

    def test_title_max_length(self):
        test_bookmark_with_long_title = create_test_bookmark(self.test_bookmarks_list, title=create_test_junk_data(MAX_TITLE_LEN + 1))

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmark_with_long_title.full_clean()
        self.fail('finish the test')


    def test_thumbnail_max_length(self):
        test_bookmark_with_long_thumbnail = create_test_bookmark(self.test_bookmarks_list, thumbnail_url=create_test_junk_data(MAX_URL_LEN + 1))

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmark_with_long_thumbnail.full_clean()
        self.fail('finish the test')
            

    def test_url_max_length(self):
        test_bookmark_with_long_url = create_test_bookmark(self.test_bookmarks_list, url=create_test_junk_data(MAX_URL_LEN + 1))

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmark_with_long_url.full_clean()
        self.fail('finish the test')

