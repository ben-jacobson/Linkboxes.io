from django.views.generic import TemplateView, ListView
from bookmarks.models import List, Bookmark

class HomePageView(TemplateView):
    template_name = 'home.html'

class LoginView(TemplateView):
    template_name = 'login.html'

class ListListView(ListView):
    template_name= 'bookmarks_list.html'
    model = List
    context_object_name = 'bookmarks_list'

    def get_queryset(self):
        query_set = Bookmark.objects.filter(_list__url_id=self.kwargs['slug'])
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_name'] = List.objects.get(url_id=self.kwargs['slug']).title
        return context
