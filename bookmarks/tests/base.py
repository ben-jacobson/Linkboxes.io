from django.contrib.auth.models import User
from bookmarks.models import Bookmark, BookmarksList
import random, string

'''
    title = models.CharField(max_length=512, blank=False)    
    thumbnail_url = models.URLField(max_length=2048, blank=False)
    url = models.URLField(max_length=2048, default='/no_thumbnail.jpg')

'''


def create_test_bookmark(   bookmarks_list, 
                            title='Testing ASDF',
                            thumbnail_url='https://via.placeholder.com/320x200', 
                            url='http://www.google.com'):
    '''
    Test Helper Function - Creates a test bookmark object and saves to test db. Returns the object
    '''                            
    test_bookmark = Bookmark(
        title=title,
        thumbnail_url=thumbnail_url,
        url=url,
        bookmarks_list=bookmarks_list
    )
    test_bookmark.save()
    return test_bookmark

def create_test_bookmarks_list(owner, title='My Test Bookmarks'):
    '''
    Test Helper Function - Creates a test bookmark list object and saves to test db. Returns the object
    '''                            
    test_bookmarks_list = BookmarksList(
        title=title,
        owner=owner
    )
    test_bookmarks_list.save()
    return test_bookmarks_list


def create_test_junk_data(len):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(len))

class test_objects_mixin():
    '''
    A lot of these test classes have the same setUp method, created a quick mixin for DRY purposes
    '''
    def setUp(self):
        self.test_user = User.objects.create_user('Joe Bloggs', 'joe@bloggs.com', 'joepassword')
        self.test_bookmarks_list = create_test_bookmarks_list(self.test_user)
        self.test_bookmark = create_test_bookmark(self.test_bookmarks_list)
