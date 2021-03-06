from django.contrib.auth.models import User
from bookmarks.models import Bookmark, List
import random, string

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
        _list=bookmarks_list
    )
    test_bookmark.save()
    return test_bookmark

def create_test_bookmarks_list(owner, title='My Test Bookmarks'):
    '''
    Test Helper Function - Creates a test bookmark list object and saves to test db. Returns the object
    '''                            
    test_bookmarks_list = List(
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
        # store these in variables so that we can login as expected
        self.test_user_name = 'JoeBloggs'
        self.test_user_email = 'joe@bloggs.com'
        self.test_user_pass = 'joepassword'

        self.test_user = User.objects.create_user(self.test_user_name, self.test_user_name, self.test_user_pass)
        self.test_bookmarks_list = create_test_bookmarks_list(self.test_user)
        self.test_bookmark = create_test_bookmark(self.test_bookmarks_list)

    def authenticate(self, username, password):
        return self.client.login(username=username, password=password)

    def log_out(self):
        return self.log_out()