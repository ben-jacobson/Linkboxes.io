from django.contrib import admin
from django.urls import include, path, re_path

from bookmarks.views import HomePageView, UserLoginView, UserSignupView, BookmarkListView, LinkBoardsListView, ListViewSet, BookmarkViewSet, get_preview
from django.contrib.auth.views import LogoutView 

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'Lists', ListViewSet)
router.register(r'Bookmark', BookmarkViewSet)

urlpatterns = [
    path('api/', include(router.urls), name='api'),

    path('admin', admin.site.urls, name='admin'),
    path('', HomePageView.as_view(), name='home'),

    re_path(r'^mylinkboxes/?$', LinkBoardsListView.as_view(), name='linkboards-listview'),
    re_path(r'^login/?$', UserLoginView.as_view(), name='login'),    
    re_path(r'^logout/?$', LogoutView.as_view(), name='logout'),
    re_path(r'^signup/?$', UserSignupView.as_view(), name='signup'),
    re_path(r'^get_preview$', get_preview, name='get-preview'),
    re_path(r'^(?P<slug>[-\w]+)/?$', BookmarkListView.as_view(), name='bookmarks-listview'),     # alternativel without optional trailing slash path('<slug:slug>', BookmarkListView.as_view(), name='bookmarks-listview'),    
]
