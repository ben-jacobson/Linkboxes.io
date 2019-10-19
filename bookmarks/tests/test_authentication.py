
from django.test import TestCase
from .base import test_objects_mixin#, create_test_bookmark, create_test_bookmarks_list, create_test_junk_data
#from bookmarks.models import Bookmark, BookmarksList

class UserAuthenticationTests(test_objects_mixin, TestCase): 
    def test_permissions_of_user(self):
        self.fail('finish the test')

    def test_authentication(self):
        self.fail('finish the test')

    def test_editing_a_bookmarkList_owned_by_user(self):
        self.fail('finish the test')

    def test_editing_a_bookmarkList_not_owned_by_user(self):
        self.fail('finish the test')