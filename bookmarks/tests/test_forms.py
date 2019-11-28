from django.test import TestCase
from .base import test_objects_mixin
from bookmarks.forms import BookmarkEditForm, BookmarkCreateForm, UserLoginForm, UserSignUpForm
from bookmarks.models import Bookmark

class BookmarkEditFormTests(test_objects_mixin, TestCase):
    def test_edit_form_renders_item_text_input(self):
        form = BookmarkEditForm()
        self.assertIn('placeholder="Title', form.as_p())
        self.assertIn('placeholder="URL', form.as_p())
        self.assertIn('placeholder="Thumbnail URL', form.as_p())

    def test_edit_form_validation_for_blank_items(self):
        form = BookmarkEditForm()
        self.assertFalse(form.is_valid())
        
    def test_edit_form_save_raises_error(self):
        with self.assertRaisesMessage(expected_exception=ValueError, expected_message='Form Saving Is Disabled'):
            BookmarkEditForm().save()

class BookmarkCreateFormTests(test_objects_mixin, TestCase):
    def test_create_form_renders_item_text_input(self):
        form = BookmarkCreateForm()
        self.assertIn('placeholder="Title', form.as_p())
        self.assertIn('placeholder="URL', form.as_p())
        self.assertIn('placeholder="Thumbnail URL', form.as_p())

    def test_create_form_validation_for_blank_items(self):
        form = BookmarkCreateForm()
        self.assertFalse(form.is_valid())
        
    def test_create_form_save(self):
        test_item_title = 'This is our test form object'
        BookmarkCreateForm(data={'title': test_item_title, 'url': 'www.google.com', 'thumbnail_url': 'www.google.com', 'list_id': self.test_bookmarks_list.url_id}).save()
        returned_bookmark = Bookmark.objects.get(title=test_item_title)
        self.assertEquals(returned_bookmark.title, test_item_title)
        
class UserLoginFormTest(test_objects_mixin, TestCase):
    def test_form_renders_item_text_input(self):
        form = UserLoginForm()
        self.assertIn('id="id_username', form.as_p())
        self.assertIn('id="id_password', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = UserLoginForm()
        self.assertFalse(form.is_valid()) 
        
    def test_valid_form(self):
        form = UserLoginForm(data={'username': self.test_user_name, 'password': self.test_user_pass})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = UserLoginForm(data={'username': self.test_user_name, 'password': ''})
        self.assertFalse(form.is_valid())
        form = UserLoginForm(data={'username': '', 'password': self.test_user_pass})
        self.assertFalse(form.is_valid())

class UserSignUpFormTest(test_objects_mixin, TestCase):
    def test_form_renders_item_text_input(self):
        form = UserSignUpForm()
        self.assertIn('id="id_username', form.as_p())
        self.assertIn('id="id_password', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = UserSignUpForm()
        self.assertFalse(form.is_valid()) 
        
    def test_valid_form(self):
        form = UserSignUpForm(data={'first_name': 'Joe', 'last_name': 'Bloggs', 'username': 'test@testerson.com.au', 'password': "AsDf1234!", 'verify_password': 'AsDf1234!'})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = UserSignUpForm(data={'username': self.test_user_name, 'password': ''})
        self.assertFalse(form.is_valid())
        form = UserSignUpForm(data={'username': '', 'password': self.test_user_pass})
        self.assertFalse(form.is_valid())

