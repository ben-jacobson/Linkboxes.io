from django.forms import ModelForm, CharField
from django.forms.fields import TextInput
#from django.core.exceptions import ValidationError
#from BaseException import ValueError

from bookmarks.models import Bookmark

class BookmarkEditForm(ModelForm):
    title = CharField(widget=TextInput(attrs={'id': 'edit-title', 'class': 'form-control', 'placeholder': 'Title',}), label='Title')
    url = CharField(widget=TextInput(attrs={'id': 'edit-url', 'class': 'form-control', 'placeholder': 'URL',}), label='URL')
    thumbnail_url = CharField(widget=TextInput(attrs={'id': 'edit-thumbnail', 'class': 'form-control', 'placeholder': 'Thumbnail URL'}), label='Thumbnail URL')
    
    class Meta:
        model = Bookmark
        fields = ('title', 'url', 'thumbnail_url', )
        '''error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }'''

    def save(self):
        raise ValueError('Form Saving Is Disabled')

