from django.contrib import admin
from django.urls import path
from bookmarks.views import HomePageView, LoginView, SignupView, ListListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
    path('<slug:slug>', ListListView.as_view(), name='bookmarks-listview'),
]


