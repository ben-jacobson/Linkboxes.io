from django.contrib import admin
from .models import Bookmark, List

class BookmarkInline(admin.TabularInline):
    model = Bookmark

@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('title', 'url_id', 'owner', )
    readonly_fields=('url_id',)

    inlines = [
        BookmarkInline,
    ]    



