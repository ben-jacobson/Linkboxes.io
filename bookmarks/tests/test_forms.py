from django.test import TestCase
from .base import test_objects_mixin
from bookmarks.forms import BookmarkEditForm, LoginForm

class BookmarkEditFormTests(test_objects_mixin, TestCase):
    def test_form_renders_item_text_input(self):
        form = BookmarkEditForm()
        self.assertIn('placeholder="Title', form.as_p())
        self.assertIn('placeholder="URL', form.as_p())
        self.assertIn('placeholder="Thumbnail URL', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = BookmarkEditForm()
        self.assertFalse(form.is_valid())
        
    def test_form_save_raises_error(self):
        with self.assertRaisesMessage(expected_exception=ValueError, expected_message='Form Saving Is Disabled'):
            BookmarkEditForm().save()

class LoginFormTest(test_objects_mixin, TestCase):
    def test_form_renders_item_text_input(self):
        form = LoginForm()
        self.assertIn('id="id_username', form.as_p())
        self.assertIn('id="id_password', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = LoginForm()
        self.assertFalse(form.is_valid()) 
        
    def test_valid_form(self):
        form = LoginForm(data={'username': self.test_user_name, 'password': self.test_user_pass})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = LoginForm(data={'username': self.test_user_name, 'password': ''})
        self.assertFalse(form.is_valid())
        form = LoginForm(data={'username': '', 'password': self.test_user_pass})
        self.assertFalse(form.is_valid())


