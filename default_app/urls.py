from django.contrib import admin
from django.urls import include, path
from bookmarks.views import HomePageView, UserLoginView, UserSignupView, BookmarkListView
from bookmarks.views import ListViewSet, BookmarkViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'Lists', ListViewSet)
router.register(r'Bookmark', BookmarkViewSet)

urlpatterns = [
    path('api/', include(router.urls), name='api'),
    #path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('login', UserLoginView.as_view(), name='login'),
    path('signup', UserSignupView.as_view(), name='signup'),
    path('<slug:slug>', BookmarkListView.as_view(), name='bookmarks-listview'),
]


