from django.forms import ModelForm, CharField, PasswordInput
from django.forms.fields import TextInput
from bookmarks.models import Bookmark

from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.models import User

class BookmarkEditForm(ModelForm):
    title = CharField(widget=TextInput(attrs={'id': 'edit-title', 'class': 'form-control', 'placeholder': 'Title',}), label='Title')
    url = CharField(widget=TextInput(attrs={'id': 'edit-url', 'class': 'form-control', 'placeholder': 'URL',}), label='URL')
    thumbnail_url = CharField(widget=TextInput(attrs={'id': 'edit-thumbnail', 'class': 'form-control', 'placeholder': 'Thumbnail URL'}), label='Thumbnail URL')
    
    class Meta:
        model = Bookmark
        fields = ('title', 'url', 'thumbnail_url', )

    def save(self):
        raise ValueError('Form Saving Is Disabled')


class UserLoginForm(AuthenticationForm):
    username = UsernameField(widget=TextInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'Email', 'autofocus': True}), label='Email address')
    password = CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', }), label="Password", strip=False)

class UserSignUpForm(ModelForm):
    first_name = UsernameField(widget=TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'First Name', 'autofocus': True}), label='First Name')
    last_name = UsernameField(widget=TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Last Name'}), label='Last Name')
    username = UsernameField(widget=TextInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'Email'}), label='Email address')
    password = CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', }), label="Password", strip=False)
    verify_password = CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Verify Password', }), label="Verify Password", strip=False)
    field_order = ('first_name', 'last_name', 'username', 'password', 'verify_password')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password')    