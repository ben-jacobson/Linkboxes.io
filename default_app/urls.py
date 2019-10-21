from django.contrib import admin
from django.urls import path
from bookmarks.views import HomePageView, BookmarksListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('<slug:slug>', BookmarksListView.as_view(), name='bookmarks-listview'),
]


