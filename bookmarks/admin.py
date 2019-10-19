from django.contrib import admin
from .models import Bookmark, BookmarksList


# Register your models here.

admin.site.register(BookmarksList)
admin.site.register(Bookmark)