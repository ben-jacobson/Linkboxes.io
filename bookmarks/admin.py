from django.contrib import admin
from .models import Bookmark, BookmarksList

class BookmarkInline(admin.TabularInline):
    model = Bookmark

#@admin.register(Bookmark)
#class BookmarkAdmin(admin.ModelAdmin):
#    list_display = ('title', 'url', 'thumbnail_url', 'bookmarks_list')

@admin.register(BookmarksList)
class BookmarksListAdmin(admin.ModelAdmin):
    list_display = ('title', 'url_id', 'owner', )
    readonly_fields=('url_id',)

    inlines = [
        BookmarkInline,
    ]    



