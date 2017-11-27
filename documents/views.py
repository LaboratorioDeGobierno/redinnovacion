from base.views import AjaxFormResponseMixin
from base.views import BaseCreateView
from base.views import BaseAjaxDeleteView

from documents.forms import FileForm
from documents.models import File
from documents.forms import PhotoForm
from documents.models import Photo
from events.models import Event
from dynamic_contents.models import DynamicContent


class FileCreateView(AjaxFormResponseMixin, BaseCreateView):
    model = File
    template_name = 'accounts/create.jade'
    form_class = FileForm

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(FileCreateView, self).get_form_kwargs()

        if self.request.method in ('POST', 'PUT'):
            kwargs['files'] = {'archive': self.request.FILES['file']}

        return kwargs

    def form_valid(self, form):
        response = super(FileCreateView, self).form_valid(form)

        if self.request.POST.get('event'):
            event = Event.objects.get(id=self.request.POST.get('event'))
            event.files.add(self.object)

        return response


class PhotoCreateView(AjaxFormResponseMixin, BaseCreateView):
    model = Photo
    template_name = 'accounts/create.jade'
    form_class = PhotoForm

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(PhotoCreateView, self).get_form_kwargs()

        if self.request.method in ('POST', 'PUT'):
            kwargs['files'] = {'photo': self.request.FILES['file']}

        return kwargs

    def form_valid(self, form):
        response = super(PhotoCreateView, self).form_valid(form)

        if self.request.POST.get('event'):
            event = Event.objects.get(id=self.request.POST.get('event'))
            event.photos.add(self.object)

        dynamic_content_id = self.request.POST.get('dynamic_content_id')
        if dynamic_content_id:
            dynamic_content = DynamicContent.objects.get(id=dynamic_content_id)
            dynamic_content.photos.add(self.object)

        return response


class FileDeleteView(BaseAjaxDeleteView):
    model = File
    permission_required = 'documents.delete_file'


class PhotoDeleteView(BaseAjaxDeleteView):
    model = Photo
    permission_required = 'documents.delete_photo'
