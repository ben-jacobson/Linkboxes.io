from django.test import TestCase
from .base import test_objects_mixin

#from bookmarks.models import Bookmark#, List
from bookmarks.forms import BookmarkEditForm#, EMPTY_ITEM_ERROR

class BookmarkEditFormTests(test_objects_mixin, TestCase):
    def test_form_renders_item_text_input(self):
        form = BookmarkEditForm()
        self.assertIn('placeholder="Title', form.as_p())
        self.assertIn('placeholder="URL', form.as_p())
        self.assertIn('placeholder="Thumbnail URL', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = BookmarkEditForm()
        self.assertFalse(form.is_valid())
        #self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])
        self.fail('Create some form validation errors and finish the test')

    def test_form_save_raises_error(self):
        with self.assertRaisesMessage(expected_exception=ValueError, expected_message='Form Saving Is Disabled'):
            BookmarkEditForm().save()