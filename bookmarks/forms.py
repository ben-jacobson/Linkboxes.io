from django.forms import ModelForm, CharField, PasswordInput
from django.forms.fields import TextInput
from bookmarks.models import Bookmark
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class BookmarkEditForm(ModelForm):
    title = CharField(widget=TextInput(attrs={'id': 'edit-title', 'class': 'form-control', 'placeholder': 'Title',}), label='Title')
    url = CharField(widget=TextInput(attrs={'id': 'edit-url', 'class': 'form-control', 'placeholder': 'URL',}), label='URL')
    thumbnail_url = CharField(widget=TextInput(attrs={'id': 'edit-thumbnail', 'class': 'form-control', 'placeholder': 'Thumbnail URL'}), label='Thumbnail URL')
    
    class Meta:
        model = Bookmark
        fields = ('title', 'url', 'thumbnail_url', )

    def save(self):
        raise ValueError('Form Saving Is Disabled')


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=TextInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'Email', 'autofocus': True}), label='Email address')
    password = CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', }), label="Password", strip=False)
