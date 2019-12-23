from django.contrib import admin
from .models import Bookmark, List

class BookmarkInline(admin.TabularInline):
    model = Bookmark
    list_display = ('id', 'title', 'thumbnail_url', 'url', )
    readonly_fields = ('id',)

@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('title', 'url_id', 'owner', )
    readonly_fields = ('url_id',)

    inlines = [
        BookmarkInline,
    ]    



