from django.forms import ModelForm, CharField, PasswordInput
from django.forms.fields import TextInput, HiddenInput
from bookmarks.models import Bookmark, List

from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.models import User

class BookmarkFormMixin(ModelForm):
    class Meta:
        model = Bookmark
        fields = ('title', 'url', 'thumbnail_url', )

class BookmarkCreateForm(BookmarkFormMixin):
    title = CharField(widget=TextInput(attrs={'id': 'create-title', 'class': 'form-control', 'placeholder': 'Title',}), label='Title')
    url = CharField(widget=TextInput(attrs={'id': 'create-url', 'class': 'form-control', 'placeholder': 'URL',}), label='URL')
    thumbnail_url = CharField(widget=TextInput(attrs={'id': 'create-thumbnail', 'class': 'form-control', 'placeholder': 'Thumbnail URL'}), label='Thumbnail URL')
    list_id = CharField(widget=HiddenInput())

    def save(self):
        # the form will save on post, we rely on the view to check that the user is logged in and is the owner
        self.instance._list = List.objects.get(url_id=self.data['list_id'])
        super().save()

class BookmarkEditForm(BookmarkFormMixin):
    title = CharField(widget=TextInput(attrs={'id': 'edit-title', 'class': 'form-control', 'placeholder': 'Title',}), label='Title')
    url = CharField(widget=TextInput(attrs={'id': 'edit-url', 'class': 'form-control', 'placeholder': 'URL',}), label='URL')
    thumbnail_url = CharField(widget=TextInput(attrs={'id': 'edit-thumbnail', 'class': 'form-control', 'placeholder': 'Thumbnail URL'}), label='Thumbnail URL')
    def save(self):
        raise ValueError('Form Saving Is Disabled') # we have some JQuery code to do this via an API call.

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