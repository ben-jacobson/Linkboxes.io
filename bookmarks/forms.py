from django.forms import ModelForm, CharField, PasswordInput, EmailField, EmailInput
from django.forms.fields import TextInput, HiddenInput
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import password_validation

from bookmarks.models import Bookmark, List
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

class LinkBoardEditForm(ModelForm):
    ''' 
    On the /Linkboards/ page or on the ListView, use this form to edit the title
    '''
    title = CharField(widget=TextInput(attrs={'id': 'edit-board-title', 'class': 'form-control',}), label='Name')

    class Meta:
        model = List
        fields = ('title', )

class LinkBoardCreateForm(ModelForm):
    ''' 
    On the /Linkboards/ page or on the ListView, use this form to create a new linkboard
    '''
    title = CharField(widget=TextInput(attrs={'id': 'create-board-title', 'class': 'form-control',}), label='Name')

    class Meta:
        model = List
        fields = ('title', )#, 'owner', )

class UserSignUpForm(UserCreationForm):
    first_name = CharField(widget=TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'First Name', 'autofocus': True}), label='First Name')
    last_name = CharField(widget=TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Last Name'}), label='Last Name')
    username = EmailField(widget=EmailInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'Email'}), label='Email Address')
    #username = UsernameField(widget=TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Username'}), label='Username')
    password1 = CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', }), label="Password", strip=False, help_text=password_validation.password_validators_help_text_html())
    password2 = CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Verify Password', }), label="Verify Password", strip=False, help_text="Enter the same password as before, for verification.")
    field_order = ('first_name', 'last_name', 'username', )

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', )