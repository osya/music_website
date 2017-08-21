from braces import views
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
    paginate_by = 10

    def get_queryset(self):
        return Album.objects.list(self.request.GET)


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

    def get_initial(self):
        initial = super(AlbumCreateView, self).get_initial()
        if self.request.GET.get('tags'):
            initial['tags'] = self.request.GET.get('tags')
        return initial


class AlbumUpdateView(views.SetHeadlineMixin, SuccessUrlMixin, generic.UpdateView):
    model = Album
    form_class = forms.AlbumForm
    headline = 'Update Album'


class AlbumDeleteView(SuccessUrlMixin, generic.DeleteView):
    model = Album
