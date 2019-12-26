from django.views.generic import TemplateView, ListView, CreateView, FormView
from django.contrib.auth.views import LoginView
from django.urls import reverse

from bookmarks.models import List, Bookmark
from bookmarks.forms import BookmarkEditForm, BookmarkCreateForm, LinkBoardEditTitleForm

from django.http import HttpResponseForbidden, HttpResponse

from rest_framework import status, viewsets, generics, permissions
from .serializers import ListSerializer, BookmarkSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth.views import LoginView
from bookmarks.forms import UserLoginForm, UserSignUpForm
from django.contrib.auth.models import User

from json import loads

'''

Django Standard Views

'''

class HomePageView(TemplateView):
    template_name = 'home.html'

class UserLoginView(LoginView):  
    # redirect url is set in SETTINGS.py
    authentication_form = UserLoginForm

    def get_success_url(self):
        return reverse('linkboards-listview')
    
class UserSignupView(CreateView):
    model = User
    template_name = 'registration/signup.html'
    form_class = UserSignUpForm

    def get_success_url(self):
        return reverse('linkboards-listview')

class BookmarkListView(CreateView, ListView): # FormView unsure if okay to mix class based views like this? Tests pass fine however. 
    form_class = BookmarkCreateForm     # there are two forms on this page, the create form uses the POST method by default in Django, the second is just UI so is passed as a context object below. 
    template_name = 'bookmarks_list.html'
    model = List
    context_object_name = 'bookmarks_list'
    
    def post(self, request, *args, **kwargs):
        # We need to overwrite our post method to check authentication and that the user is correct
        form = self.get_form()
        list_obj = List.objects.get(url_id=self.kwargs['slug'])

        if request.user != list_obj.owner:  # prevent user from modifying lists they don't own
            return HttpResponseForbidden()
            
        if form.data['list_id'] != list_obj.url_id:  # to stop users from injecting into lists other than ones on this page
            return HttpResponseForbidden()
   
        return super().post(request, *args, **kwargs)

    def get_initial(self):  # this is how you prepopulate form data on runtime
        return {'list_id': self.kwargs['slug']}

    def get_success_url(self):
        return reverse('bookmarks-listview', kwargs={'slug': self.kwargs['slug']})

    def get_queryset(self):
        query_set = Bookmark.objects.filter(_list__url_id=self.kwargs['slug'])
        return query_set

    def get_context_data(self, **kwargs):
        # kwargs['edit_bookmark_form'] = BookmarkEditForm   # This is how the parent method does it, 
        context = super().get_context_data(**kwargs)
        list_obj = List.objects.get(url_id=self.kwargs['slug'])
        context['list_slug'] = list_obj.url_id
        context['list_name'] = list_obj.title
        context['edit_bookmark_form'] = BookmarkEditForm 
        return context

class LinkBoardsListView(FormView, ListView):
    template_name = 'linkboards_list.html'
    model = List
    context_object_name = 'linkboards'
    form_class = LinkBoardEditTitleForm

    def get_queryset(self):
        return List.objects.filter(owner=self.request.user.id)

    def get_success_url(self):
        return reverse('linkboards-listview')    

    def post(self, request, *args, **kwargs):
        # the way this view works is that we use the formview to render a form with the CSRF token, 
        # but the pages AJAX request to DRF does the update work. 
        # so the server doesn't need to do anything except return a 204. 
        # I haven't tried returning a 200 yet because this may mess with the AJAX request since there is no return data
        return HttpResponse(status=204)

'''class LinkBoardsListView(ModelFormMixin, ListView):
    form_class = LinkBoardEditTitleForm
    template_name = 'linkboards_list.html'
    model = List
    context_object_name = 'linkboards'

    def get_success_url(self):
        return reverse('linkboards-listview')

    def get_object(self,queryset=None):  
        queryset = List.objects.filter(owner=self.request.user.id)
        return super(LinkBoardsListView, self).get_object(queryset))

    def get_context_data(self, **kwargs):

        context = ModelFormMixin.get_context_data(**kwargs)
        context = ListView.get_context_data(**context)
        return context

    def get_queryset(self):
        return List.objects.filter(owner=self.request.user.id)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, this is for the edit LinkBoard form
        """
        form = self.get_form()
        self.form = form

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

'''

'''

Django Rest Framework Views

'''

class IsListOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any safe request for Lists,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user

class IsBookmarkOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to read and edit it.
    Looks at the objects foreign key owner to determine who is allowed to read and edit
    """

    def has_object_permission(self, request, view, obj):
        # Bookmark is owned by a List, uses the List user to determine ownership. Safe methods are conditionally allowed based on user
        list_owner = List.objects.get(id=obj._list_id).owner
        return list_owner == request.user        
        
class ListViewSet(generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    '''
    API endpoint that allows Lists to be retrieved, but does not allow all lists to be viewed in a list.
    '''
    permission_classes = [IsListOwnerOrReadOnly]

    queryset = List.objects.all()
    serializer_class = ListSerializer
    lookup_field = 'url_id' 

    @action(detail=True, methods=['PATCH'])  # we can call this method when re-ordering bookmarks via API calls
    def reorder(self, request, *args, **kwargs):
        list_obj = self.get_object()

        if list_obj.owner == request.user: # for some reason DRF @action decorator ignores the permission classes
            request_body = loads(request.body)
            new_order = request_body['new_order']
            list_obj.set_bookmark_order(new_order)
            return Response('status', status=status.HTTP_200_OK)
        else:
            return Response('status', status=status.HTTP_403_FORBIDDEN)


class BookmarkViewSet(generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    '''
    API endpoint that allows  Bookmarks to be retrieved, but does not allow all bookmarks to be viewed in a list.
    '''
    permission_classes = [IsBookmarkOwner]

    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer