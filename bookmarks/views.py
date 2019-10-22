from django.views.generic import TemplateView, ListView
from bookmarks.models import BookmarksList, Bookmark

class HomePageView(TemplateView):
    template_name = 'home.html'

class BookmarksListView(ListView):
    template_name= 'bookmarks_list.html'
    model = BookmarksList
    context_object_name = 'bookmarks_list'

    def get_queryset(self):
        query_set = Bookmark.objects.filter(bookmarks_list__url_id=self.kwargs['slug'])
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_name'] = BookmarksList.objects.get(url_id=self.kwargs['slug']).title
        return context
