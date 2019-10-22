from django.test import TestCase
from .base import test_objects_mixin, create_test_bookmark, create_test_bookmarks_list, create_test_junk_data
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

    def test_create_bookmarks_list_without_title_throws_validation_error(self):
        '''
        Unit Test - URL and Title are mandatory fields
        '''    
        test_bookmarks_list_without_title = create_test_bookmarks_list(owner=self.test_user, title='')

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmarks_list_without_title.full_clean()

    def test_create_bookmarks_list_creates_id(self):
        '''
        Unit Test - Test the model generated tiny url BookmarksList.save()
        '''    
        # expected output is a 5 digit code. 
        bookmarks_list_obj = BookmarksList.objects.get(title=self.test_bookmarks_list.title)  
        self.assertEqual(len(bookmarks_list_obj.url_id), 5)      

        # check that the string is alphanumeric
        self.assertTrue(bookmarks_list_obj.url_id.isalnum())

    def test_create_bookmarks_id_must_be_unique(self):
        '''
        Unit Test - Test the model generated tiny url BookmarksList.save()
        '''    
        # running the save function will generate the hash, so to test this we'll instead run the validate_unique and verify that it generates the appropraite exception
        bookmarks_list_obj = BookmarksList.objects.get(title=self.test_bookmarks_list.title)  
        comparison_list = BookmarksList(title='adsf', url_id=bookmarks_list_obj.url_id)

        with self.assertRaises(ValidationError):
            comparison_list.validate_unique()

    def test_create_bookmarks_id_full_clean_raises_exception(self):
        # virtually the same as above, except with full_clean()
        bookmarks_list_obj = BookmarksList.objects.get(title=self.test_bookmarks_list.title)  
        comparison_list = BookmarksList(title='adsf', url_id=bookmarks_list_obj.url_id)

        with self.assertRaises(ValidationError):
            comparison_list.full_clean()

    def test_title_max_length(self):
        test_bookmarks_list_with_long_title = create_test_bookmarks_list(owner=self.test_user, title=create_test_junk_data(MAX_TITLE_LEN + 1))

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmarks_list_with_long_title.full_clean()

    def test_model_save_feature_doesnt_reroll_urlid(self):
        '''
        Unit Test - fix a bug early on where the url_id field (slug) was rerolled on every save.
        '''
        # create a new test_bookmarks_list
        test_bookmarks_list = create_test_bookmarks_list(self.test_user)

        # functionan automatically calls save, so we now record what the id is after first save
        url_first_save = test_bookmarks_list.url_id

        # make a change to it, save it and record the url again
        test_bookmarks_list.title = 'new title'
        test_bookmarks_list.save()
        url_second_save = test_bookmarks_list.url_id

        # they should be the same
        self.assertEqual(url_first_save, url_second_save)          

class UserModelTests(test_objects_mixin, TestCase): 
    def test_create_user(self):
        '''
        Unit Test - User successfully creates a bookmark with a valid title, url and picture
        '''   
        self.assertEquals(self.test_bookmark, Bookmark.objects.get(title=self.test_bookmark.title))
        self.fail('finish the test')

    def test_create_user_without_password_throws_validation_error(self):
        '''
        Unit Test - URL and Title are mandatory fields
        '''    
        test_bookmark_without_title = create_test_bookmark(self.test_bookmarks_list, title='')

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmark_without_title.full_clean()
        self.fail('finish the test')

    def test_create_user_without_username_throws_validation_error(self):
        '''
        Unit Test - URL and Title are mandatory fields
        '''    
        test_bookmark_without_title = create_test_bookmark(self.test_bookmarks_list, title='')

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmark_without_title.full_clean()
        self.fail('finish the test')

