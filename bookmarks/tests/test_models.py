from django.test import TestCase
from .base import test_objects_mixin, create_test_bookmark, create_test_junk_data
from bookmarks.models import Bookmark

from django.core.exceptions import ValidationError
#from django.db import IntegrityError

#User (ID, manyToOne relationships with BookmarksList)
#BookmarksList (Url, manyToOne relationships with links, Privacy flag, pin_code_for_editing)
#Bookmarks (Title, URL, Picture URL)



# Create your tests here.
class BookmarkModelTests(test_objects_mixin, TestCase): 
    def test_create_bookmark(self):
        '''
        Unit Test - User successfully creates a bookmark with a valid title, url and picture
        '''   
        self.assertEquals(self.test_bookmark, Bookmark.objects.get(title=self.test_bookmark.title))

    def test_create_bookmark_without_title_throws_validation_error(self):
        '''
        Unit Test - URL and Title are mandatory fields
        '''    
        test_bookmark_without_title = create_test_bookmark(title='')

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmark_without_title.full_clean()

    def test_create_bookmark_without_url_throws_validation_error(self):
        '''
        Unit Test - URL and Title are mandatory fields
        '''        
        test_bookmark_without_url = create_test_bookmark(url='')

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmark_without_url.full_clean()

    # We had model validation for correct urls and image types, but playing with the model validation proved to be to finnicky. Plus it would mean less flexibility in future migrations. Best that we handle all validation of this data at the form layer. 

    def test_create_bookmark_without_picture(self):
        '''
        Unit Test - Users can create a bookmark without a picture, it should default to a placeholder image
        '''
        test_bookmark_without_image = create_test_bookmark(thumbnail_url='')
        test_bookmark_without_image.save()
        self.assertEqual(test_bookmark_without_image.thumbnail_url, '/no_thumbnail.jpg')

    def test_title_max_length(self):
        test_bookmark_with_long_title = create_test_bookmark(title=create_test_junk_data(512 + 1))

        # does it raise exceptions on full_clean and save? 
        with self.assertRaises(ValidationError):
            test_bookmark_with_long_title.full_clean()

        self.fail('finish the test')

    def test_image_max_length(self):
        self.fail('finish the test')

    def test_url_max_length(self):
        self.fail('finish the test')