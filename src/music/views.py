from braces import views
from django.db.models import Count
from django.urls import reverse
from django.views import generic

from music import forms
from music.models import Album


class SuccessUrlMixin(generic.base.View):
    def get_success_url(self):
        url = reverse('music:album_list')
        query = self.request.GET.urlencode()
        if query:
            url = f'{url}?{query}'
        return url


class AlbumListView(generic.ListView):
    model = Album
    paginate_by = 10

    def get_queryset(self):
        queryset = super(AlbumListView, self).get_queryset()
        tags = self.request.GET.get('tags')
        if tags:
            tags = tags.split(',')
            queryset = queryset.filter(tags__name__in=tags).distinct()
        queryset = queryset.annotate(song_count=Count('songs'))
        return queryset


class AlbumDetailView(generic.DetailView, generic.UpdateView):
    model = Album
    http_method_names = ['get', 'post']
    form_class = forms.AlbumFavoriteForm
    template_name = 'music/album_detail.html'

    def get_success_url(self):
        return reverse('music:album_detail', kwargs=self.kwargs)


class AlbumCreateView(views.SetHeadlineMixin, SuccessUrlMixin, generic.CreateView):
    model = Album
    form_class = forms.AlbumForm
    headline = 'Add Album'


class AlbumUpdateView(views.SetHeadlineMixin, SuccessUrlMixin, generic.UpdateView):
    model = Album
    form_class = forms.AlbumForm
    headline = 'Update Album'


class AlbumDeleteView(SuccessUrlMixin, generic.DeleteView):
    model = Album
