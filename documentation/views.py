# -*- coding: utf-8 -*-
""" Views for the documentation application. """
# standard library

# django
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.db.models import Q
from django.http.response import JsonResponse
from django.utils.text import slugify
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.detail import SingleObjectMixin

# models
from .models import DocumentationFile
from .models import DocumentationSearch
from .models import DocumentationSearchLog
from .models import Methodology
from .models import Publication
from .models import Tool
from users.models import User

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseDetailView
from base.views import BaseListView
from base.views import BaseUpdateView
from base.views import DownloadView

# forms
from .forms import DocumentationFileForm
from .forms import DocumentationTagsForm
from .forms import MethodologyForm
from .forms import PublicationForm
from .forms import ToolForm

# utils
from documentation import utils
from base import view_utils

# itertools
from itertools import chain


class DocumentationView(TemplateView):
    template_name = "documentation/methodology_tool_list.jade"


class DocumentationListView(BaseListView):
    accepted_ordering = ['title', 'created_at']
    active_tab = None
    model = None
    ordering = '-created_at'
    template_name = None

    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseListView, self).dispatch(*args, **kwargs)

    def get_ordering(self):
        """
        Return the field or fields to use for ordering the queryset.
        """
        ordering = self.request.GET.get('o_', self.ordering)
        if self.is_valid_ordering(ordering):
            self.ordering = ordering
        return (self.ordering, )

    def is_valid_ordering(self, ordering):
        """
        Check if ordering parameter is valid.
        """
        if ordering and ordering.startswith('-'):
            ordering = ordering[1:]
        return ordering in self.accepted_ordering

    def get_queryset(self):
        """Returns documentation """
        ordering = self.get_ordering()
        return self.model.objects.all().order_by(*ordering)

    def get_context_data(self, **kwargs):
        context = super(DocumentationListView, self).get_context_data(**kwargs)

        # add active tab
        context['active_tab'] = self.active_tab
        context['navbar_active'] = 'documentation'
        context['o_'] = self.request.GET.get('o_', self.ordering)
        page = self.request.GET.get('by')
        try:
            context['by'] = int(page)
        except:
            context['by'] = self.paginate_by
        context['title'] = u'Recursos'
        context['subtitle'] = (
            u'Aquí encontrarás distintos tipos de materiales, herramientas y'
            u' metodologías de innovación que podrás aplicar en tu día a día'
            u' o bien para que puedas realizar tus propios talleres y'
            u' encuentros; así como publicaciones de temáticas relacionadas'
            u' a la innovación en el sector público.'
        )
        return context


class MethodologyListView(DocumentationListView):
    """
    View for displaying a list of Methodologies.
    """
    model = Methodology
    template_name = 'documentation/methodology/list.jade'
    active_tab = 'tools'
    paginate_by = 4

    def get_template_names(self):
        if self.request.is_ajax():
            return 'documentation/methodology/more-list.jade'
        return self.template_name

    def get_context_data(self, **kwargs):
        context = super(MethodologyListView, self).get_context_data(**kwargs)

        # add to the context 5 highlighted publications
        context['publications'] = Publication.objects.filter(
            highlighted=True
        ).order_by('created_at')[:5]
        return context


class ToolListView(DocumentationListView):
    """
    View for displaying a list of tools.
    """
    model = Tool
    template_name = 'documentation/tool/list.jade'
    active_tab = 'tools'


class PublicationListView(DocumentationListView):
    """
    View for displaying a list of publications.
    """
    model = Publication
    template_name = 'documentation/publication/list.jade'
    active_tab = 'publications'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(PublicationListView, self).get_context_data(**kwargs)
        context['title'] = u'Publicaciones'
        context['subtitle'] = (
            u'Descarga publicaciones sobre distintas temáticas relacionadas'
            u' a la innovación en el sector público.'
        )
        return context


class DocumentationDetailView(BaseDetailView):
    model = None
    template_name = None
    active_tab = None

    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DocumentationDetailView, self).get_context_data(
            **kwargs
        )
        context['active_tab'] = self.active_tab
        context['navbar_active'] = 'documentation'
        context['title'] = u'Metodologías y herramientas'
        context['subtitle'] = (
            u'Encuentra herramientas y metodologías de innovación que podrás'
            u' aplicar en tu trabajo del día a día, así como también para'
            u' realizar tus propios talleres y encuentros.'
        )
        return context


class MethodologyDetailView(DocumentationDetailView):
    """
    A view for displaying a single methodology
    """
    active_tab = 'tools'
    model = Methodology
    template_name = 'documentation/methodology/detail.jade'


class ToolDetailView(DocumentationDetailView):
    """
    A view for displaying a single tool
    """
    active_tab = 'tools'
    model = Tool
    template_name = 'documentation/tool/detail.jade'


class PublicationDetailView(DocumentationDetailView):
    """
    A view for displaying a single publication
    """
    active_tab = 'publications'
    model = Publication
    template_name = 'documentation/publication/detail.jade'

    def get_context_data(self, **kwargs):
        context = super(PublicationDetailView, self).get_context_data(**kwargs)
        context['highlighted_publications'] = self.object.get_highlights()
        context['title'] = u'Publicaciones'
        context['subtitle'] = (
            u'Descarga publicaciones sobre distintas temáticas relacionadas'
            u' a la innovación en el sector público.'
        )
        return context


class DocumentationCreateView(BaseCreateView):
    """
    An abstract view for creating a documentation
    """

    def post(self, request, *args, **kwargs):
        # set object to null
        self.object = None

        # get documentation file form, to save files in a documentation
        documentation_file_form = DocumentationFileForm(
            request.POST,
            request.FILES,
        )

        # get tags form
        tags_form = DocumentationTagsForm(
            request.POST,
        )

        # get model form
        form = self.get_form()

        # check if forms are valid
        if (
            form.is_valid()
            and documentation_file_form.is_valid()
            and tags_form.is_valid()
        ):
            return self.form_valid(form, documentation_file_form, tags_form)
        else:
            return self.form_invalid(form, documentation_file_form, tags_form)

    def form_valid(self, form, documentation_form, tags_form):
        # save documentation files and then add to documentation
        documentation_file = documentation_form.save()

        # save object instance and add documentation files
        self.object = form.save(commit=False)
        self.object.documentation_file = documentation_file
        self.object.save()

        # tags
        tags = tags_form.cleaned_data['tags'].split(',')
        self.object.add_tags(tags)

        view_utils.add_success_message(
            self.request,
            u"Creación exitosa"
        )

        return super(DocumentationCreateView, self).form_valid(form)

    def form_invalid(self, form, documentation_form, tags_form):
        forms = [form, documentation_form, tags_form]
        for _form in forms:
            view_utils.add_form_error_messages(
                self.request,
                _form
            )
        return super(DocumentationCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(DocumentationCreateView, self).get_context_data(
            **kwargs
        )
        context['documentation_file_form'] = DocumentationFileForm()
        context['tags_form'] = DocumentationTagsForm()
        context['navbar_active'] = 'documentation'
        context['navbar_active'] = 'documentation'
        return context

    def get_success_url(self):
        return self.object.get_absolute_url()


class MethodologyCreateView(DocumentationCreateView):
    """
    A view for creating a methodology
    """
    model = Methodology
    form_class = MethodologyForm
    template_name = 'documentation/methodology/create.jade'
    permission_required = 'documentation.add_methodology'

    def get_context_data(self, **kwargs):
        context = super(MethodologyCreateView, self).get_context_data(
            **kwargs
        )
        context['cancel_url'] = reverse('methodology_list')
        return context


class ToolCreateView(DocumentationCreateView):
    """
    A view for creating a tool
    """
    model = Tool
    form_class = ToolForm
    template_name = 'documentation/tool/create.jade'
    permission_required = 'documentation.add_tool'

    def get_context_data(self, **kwargs):
        context = super(ToolCreateView, self).get_context_data(
            **kwargs
        )
        context['cancel_url'] = reverse('methodology_list')
        return context

    def form_valid(self, form, documentation_form, tags_form):
        response = super(ToolCreateView, self).form_valid(
            form,
            documentation_form,
            tags_form
        )

        methodology_pk = self.kwargs.get('methodology_pk')
        if methodology_pk:
            methodology = Methodology.objects.get(id=methodology_pk)
            print 'ok'
            methodology.tools.add(self.object)

        return response


class PublicationCreateView(DocumentationCreateView):
    """
    A view for creating a Publication
    """
    model = Publication
    form_class = PublicationForm
    template_name = 'documentation/publication/create.jade'
    permission_required = 'documentation.add_publication'

    def get_context_data(self, **kwargs):
        context = super(PublicationCreateView, self).get_context_data(
            **kwargs
        )
        context['cancel_url'] = reverse('publication_list')
        return context


class DocumentationUpdateView(BaseUpdateView):
    """
    A view for editing a methodology
    """
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # get documentation file form, to save files in a documentation
        documentation_file_form = DocumentationFileForm(
            request.POST,
            request.FILES,
            instance=self.object.documentation_file
        )

        # get tags form
        tags_form = DocumentationTagsForm(
            request.POST,
        )

        # get model form
        form = self.get_form()

        # check if both forms are valid
        if (
            form.is_valid()
            and documentation_file_form.is_valid()
            and tags_form.is_valid()
        ):
            return self.form_valid(form, documentation_file_form, tags_form)
        else:
            return self.form_invalid(form, documentation_file_form, tags_form)

    def form_valid(self, form, documentation_form, tags_form):
        # save documentation files and then add to documentation
        documentation_file = documentation_form.save()

        # save object instance and add documentation files
        self.object = form.save(commit=False)
        self.object.documentation_file = documentation_file
        self.object.save()

        # tags
        tags = tags_form.cleaned_data['tags'].split(',')
        self.object.add_tags(tags)

        view_utils.add_success_message(
            self.request,
            u"Actualización exitosa"
        )

        return super(DocumentationUpdateView, self).form_valid(form)

    def form_invalid(self, form, documentation_form, tags_form):
        forms = [form, documentation_form, tags_form]
        for _form in forms:
            view_utils.add_form_error_messages(self.request, _form)
        return super(DocumentationUpdateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(DocumentationUpdateView, self).get_context_data(
            **kwargs
        )
        context['documentation_file_form'] = DocumentationFileForm(
            instance=self.object.documentation_file
        )
        context['tags_form'] = DocumentationTagsForm(
            initial={
                'tags': self.object.get_string_tags(),
            },
        )
        context['navbar_active'] = 'documentation'
        return context

    def get_success_url(self):
        return self.object.get_absolute_url()


class MethodologyUpdateView(DocumentationUpdateView):
    """
    A view for editing a methodology
    """
    model = Methodology
    form_class = MethodologyForm
    template_name = 'documentation/methodology/update.jade'
    permission_required = 'documentation.change_methodology'


class ToolUpdateView(DocumentationUpdateView):
    """
    A view for editing a tool
    """
    model = Tool
    form_class = ToolForm
    template_name = 'documentation/tool/update.jade'
    permission_required = 'documentation.change_tool'


class PublicationUpdateView(DocumentationUpdateView):
    """
    A view for editing a publication
    """
    model = Publication
    form_class = PublicationForm
    template_name = 'documentation/publication/update.jade'
    permission_required = 'documentation.change_publication'


class MethodologyDeleteView(BaseDeleteView):
    """
    A view for deleting a methodology
    """
    model = Methodology
    template_name = 'documentation/methodology/delete.jade'
    permission_required = 'documentation.delete_methodology'

    def get_success_url(self):
        return reverse('methodology_list')

    def get_context_data(self, **kwargs):
        context = super(MethodologyDeleteView, self).get_context_data(**kwargs)
        context['navbar_active'] = 'documentation'
        return context


class ToolDeleteView(BaseDeleteView):
    """
    A view for deleting a tool
    """
    model = Tool
    template_name = 'documentation/tool/delete.jade'
    permission_required = 'documentation.delete_tool'

    def get_success_url(self):
        return reverse('tool_list')

    def get_context_data(self, **kwargs):
        context = super(ToolDeleteView, self).get_context_data(**kwargs)
        context['navbar_active'] = 'documentation'
        return context


class PublicationDeleteView(BaseDeleteView):
    """
    A view for deleting a publication
    """
    model = Publication
    template_name = 'documentation/publication/delete.jade'
    permission_required = 'documentation.delete_publication'

    def get_success_url(self):
        return reverse('publication_list')

    def get_context_data(self, **kwargs):
        context = super(PublicationDeleteView, self).get_context_data(**kwargs)
        context['navbar_active'] = 'documentation'
        return context


class DownloadDocumentationFileView(SingleObjectMixin, DownloadView):
    """
    DocumentationFile Download View
    """
    model = DocumentationFile
    slug_field = 'hash_id'
    slug_url_kwarg = 'hash_id'
    use_xsendfile = False

    def get_contents(self):
        # get file with a generic method
        return self.get_object().get_file()

    def get_filename(self):
        # get filename
        return slugify(self.get_object().name) + self.get_extension()

    def get_extension(self):
        # get file extension
        return self.get_object().extension()

    def logging(self):
        # log user download
        self.get_object().log_download(self.request.user)


class DocumentationSearchView(BaseListView):
    template_name = "documentation/search/list.jade"
    model = None
    ordering = 'title'
    paginate_by = 10
    active = 'documentation'
    accepted_ordering = ['title']
    search = None
    type_search = 'all'
    count = {}

    def dispatch(self, *args, **kwargs):
        self.type_search = self.request.GET.get('type', self.type_search)

        if self.type_search == 'methodology':
            self.model = Methodology
            self.active = 'methodology'
        elif self.type_search == 'tool':
            self.model = Tool
            self.active = 'tool'
        elif self.type_search == 'publication':
            self.model = Publication
            self.active = 'publication'

        self.check_permission_required()
        return super(BaseListView, self).dispatch(*args, **kwargs)

    def get_ordering(self):
        """
        Return the field or fields to use for ordering the queryset.
        """
        ordering = self.request.GET.get('o_', self.ordering)
        if self.is_valid_ordering(ordering):
            self.ordering = ordering
        return (self.ordering, )

    def is_valid_ordering(self, ordering):
        """
        Check if ordering parameter is valid.
        """
        if ordering and ordering.startswith('-'):
            ordering = ordering[1:]
        return ordering in self.accepted_ordering

    def get_queryset(self):
        """
        get_queryset override
        """
        # register search
        self.register_search()

        # get ordering
        ordering = self.get_ordering()

        # filter and order multiple models
        models = [Publication, Tool, Methodology]
        objects = []
        self.count['total_count'] = 0

        for model in models:
            qs = self.get_filter_queryset(model)

            # add counters
            name = model.__name__.lower()
            key = "{}_count".format(name)
            count = qs.count()
            self.count[key] = count
            if name == self.active or self.active == 'documentation':
                self.count['total_count'] += count

            # merge list
            if not self.model or model == self.model:
                objects = list(chain(objects, qs))

        # sort queryset
        objects = utils.order_queryset(objects, ordering)

        return objects

    def register_search(self):
        """
        Records the searches performed by users
        """

        # filter search
        q = self.request.GET.get('q')
        if q and self.request.user.is_authenticated():
            search, created = DocumentationSearch.objects.get_or_create(
                search=q
            )
            self.search = search

            # log search
            DocumentationSearchLog.objects.create(
                documentation_search=search,
                user=self.request.user
            )

    def get_filter_queryset(self, model=None):
        """
        Filter documentation model.
        """
        model = model if model else self.model
        q = self.request.GET.get('q')
        qs = model.objects.all()
        if q:
            qs = qs.filter(
                Q(title__unaccent__icontains=q)
                | Q(tags__name__unaccent__icontains=q)
            ).distinct()

        language = self.request.GET.get('language')
        if language:
            qs = qs.filter(language=language)

        return qs

    def get_context_data(self, **kwargs):
        context = super(DocumentationSearchView, self).get_context_data(
            **kwargs
        )

        # add documentation count per model
        for key, value in self.count.iteritems():
            context[key] = value

        context['title'] = u'Resultado de búsqueda: {} ({} documentos)'.format(
            self.request.GET.get('q'),
            context.get('total_count', 0),
        )

        # order
        if self.is_valid_ordering(self.request.GET.get('o_')):
            context['o_'] = self.request.GET.get('o_')

        context['language'] = self.request.GET.get('language')
        # set active documentation
        context['active'] = self.active

        # related searches
        context['searches'] = (
            DocumentationSearch.objects.all().annotate(
                search_count=Count('documentationsearchlog')
            ).order_by('-highlighted', '-search_count')[:5]
        )

        context['navbar_active'] = 'documentation'

        # add users who already searched the same query
        if self.search:
            context['search_users'] = (
                User.objects.filter(
                    documentation_searched__documentation_search=self.search
                ).exclude(id=self.request.user.id).distinct()[:5]
            )
        return context


class DocumentationShareView(BaseDetailView):
    model = None

    def post(self, request, *args, **kwargs):
        res = {}
        if request.is_ajax():
            message = request.POST.get('message', '')
            users = request.POST.getlist('users')
            if len(users):
                doc = self.get_object()
                doc.share(request.user, users, message, request.is_secure())
                res['status'] = 'ok'
            else:
                res['status'] = 'error'
                res['error'] = 'no users'
        else:
            res['status'] = 'error'
            res['error'] = 'Request must be AJAX'
        return JsonResponse(res)

    def get(self, request, *args, **kwargs):
        return redirect(self.get_object().get_absolute_url())


class MethodologyShareView(DocumentationShareView):
    model = Methodology


class ToolShareView(DocumentationShareView):
    model = Tool


class PublicationShareView(DocumentationShareView):
    model = Publication
