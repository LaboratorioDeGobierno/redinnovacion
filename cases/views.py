# -*- coding: utf-8 -*-
""" Views for the cases application. """
# standard library

# django
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.db.models import Q
from django.http.response import JsonResponse
from django.shortcuts import redirect

# views
from base.views import AjaxFormResponseMixin
from base.views import BaseAjaxDeleteView
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseDetailView
from base.views import BaseListView
from base.views import BaseUpdateView

# models
from cases.models import Case
from cases.models import CaseSearch
from cases.models import CaseSearchLog
from documents.models import File
from users.models import User

# forms
from cases.forms import CaseTagsForm
from cases.forms import CaseForm
from documents.forms import FileForm

# utils
from base import view_utils


class CaseListView(BaseListView):
    accepted_ordering = ['title', 'created_at']
    model = Case
    ordering = '-created_at'
    template_name = 'cases/list.jade'

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
        context = super(CaseListView, self).get_context_data(**kwargs)
        context['navbar_active'] = 'cases'
        context['active_tab'] = 'cases'
        context['o_'] = self.request.GET.get('o_', self.ordering)
        page = self.request.GET.get('by')
        try:
            context['by'] = int(page)
        except:
            context['by'] = self.paginate_by
        return context


class CaseDetailView(BaseDetailView):
    model = Case
    template_name = 'cases/detail.jade'

    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CaseDetailView, self).get_context_data(**kwargs)
        context['navbar_active'] = 'cases'
        context['active_tab'] = 'cases'
        return context


class CaseCreateView(BaseCreateView):
    """
    A view for creating a case
    """
    model = Case
    form_class = CaseForm
    template_name = 'cases/create.jade'
    permission_required = 'cases.add_case'

    def post(self, request, *args, **kwargs):
        # set object to null
        self.object = None

        # get tags form
        tags_form = CaseTagsForm(
            request.POST,
        )

        # get model form
        form = self.get_form()

        # check if forms are valid
        if (
            form.is_valid()
            and tags_form.is_valid()
        ):
            return self.form_valid(form, tags_form)
        else:
            return self.form_invalid(form, tags_form)

    def form_valid(self, form, tags_form):
        # save object instance and add documentation files
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        # tags
        tags = tags_form.cleaned_data['tags'].split(',')
        self.object.add_tags(tags)

        view_utils.add_success_message(
            self.request,
            u"Creación exitosa"
        )

        return super(CaseCreateView, self).form_valid(form)

    def form_invalid(self, form, documentation_form, tags_form):
        forms = [form, documentation_form, tags_form]
        for _form in forms:
            view_utils.add_form_error_messages(
                self.request,
                _form
            )
        return super(CaseCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(CaseCreateView, self).get_context_data(
            **kwargs
        )
        context['tags_form'] = CaseTagsForm()
        context['navbar_active'] = 'cases'
        context['active_tab'] = 'cases'
        return context

    def get_success_url(self):
        return reverse('case_update', args=(self.object.id, ))


class CaseUpdateView(BaseUpdateView):
    """
    A view for editing a case
    """
    model = Case
    form_class = CaseForm
    template_name = 'cases/update.jade'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.request.user.is_authenticated():
            raise PermissionDenied

        if not self.request.user.is_staff:
            if self.request.user.id != self.object.author_id:
                raise PermissionDenied

        return super(CaseUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # set object to null
        self.object = self.get_object()

        # get tags form
        tags_form = CaseTagsForm(
            request.POST,
        )

        # get model form
        form = self.get_form()

        # check if forms are valid
        if (
            form.is_valid()
            and tags_form.is_valid()
        ):
            return self.form_valid(form, tags_form)
        else:
            return self.form_invalid(form, tags_form)

    def form_valid(self, form, tags_form):
        # save object instance and add documentation files
        self.object = form.save(commit=False)
        self.object.editor = self.request.user
        self.object.save()

        # tags
        tags = tags_form.cleaned_data['tags'].split(',')
        self.object.add_tags(tags)

        view_utils.add_success_message(
            self.request,
            u"Actualización exitosa"
        )

        return super(CaseUpdateView, self).form_valid(form)

    def form_invalid(self, form, documentation_form, tags_form):
        forms = [form, documentation_form, tags_form]
        for _form in forms:
            view_utils.add_form_error_messages(
                self.request,
                _form
            )
        return super(CaseUpdateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(CaseUpdateView, self).get_context_data(
            **kwargs
        )
        context['tags_form'] = CaseTagsForm(
            initial={
                'tags': self.object.get_string_tags(),
            },
        )
        context['navbar_active'] = 'cases'
        context['active_tab'] = 'cases'
        return context

    def get_success_url(self):
        return self.object.get_absolute_url()


class CaseDeleteView(BaseDeleteView):
    """
    A view for deleting a case
    """
    model = Case
    template_name = 'cases/delete.jade'
    permission_required = 'cases.delete_case'

    def get_success_url(self):
        return reverse('case_list')

    def get_context_data(self, **kwargs):
        context = super(CaseDeleteView, self).get_context_data(**kwargs)
        context['navbar_active'] = 'cases'
        context['active_tab'] = 'cases'
        return context


class CaseSearchView(BaseListView):
    template_name = 'cases/search.jade'
    model = Case
    ordering = '-created_at'
    paginate_by = 10
    accepted_ordering = ['title', 'created_at']
    search = None

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
        """
        get_queryset override
        """
        # register search
        self.register_search()

        # get ordering
        ordering = self.get_ordering()

        qs = self.get_filter_queryset()
        return qs.order_by(*ordering)

    def register_search(self):
        """
        Records the searches performed by users
        """

        # filter search
        q = self.request.GET.get('q')
        if q and self.request.user.is_authenticated():
            search, created = CaseSearch.objects.get_or_create(
                search=q
            )
            self.search = search

            # log search
            CaseSearchLog.objects.create(
                case_search=search,
                user=self.request.user
            )

    def get_filter_queryset(self, model=None):
        """
        Filter case model.
        """
        q = self.request.GET.get('q')
        qs = self.model.objects.all()
        if q:
            qs = qs.filter(
                Q(title__unaccent__icontains=q)
                | Q(tags__name__unaccent__icontains=q)
            ).distinct()
        return qs

    def get_context_data(self, **kwargs):
        context = super(CaseSearchView, self).get_context_data(
            **kwargs
        )

        # add documentation count per model
        context['case_count'] = self.model.objects.all().count()

        # order
        if self.is_valid_ordering(self.request.GET.get('o_')):
            context['o_'] = self.request.GET.get('o_')

        # related searches
        context['searches'] = (
            CaseSearch.objects.all().annotate(
                search_count=Count('casesearchlog')
            ).order_by('-highlighted', '-search_count')[:5]
        )

        context['navbar_active'] = 'cases'
        context['active_tab'] = 'cases'

        # add users who already searched the same query
        if self.search:
            context['search_users'] = (
                User.objects.filter(
                    case_searched__case_search=self.search
                ).exclude(id=self.request.user.id).distinct()[:5]
            )
        return context


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

        if self.request.POST.get('case'):
            case = Case.objects.get(id=self.request.POST.get('case'))
            case.attachments.add(self.object)

        return response


class FileDeleteView(BaseAjaxDeleteView):
    model = File
    permission_required = 'documents.delete_file'


class CaseShareView(BaseDetailView):
    model = Case

    def post(self, request, *args, **kwargs):
        res = {}
        if request.is_ajax():
            message = request.POST.get('message', '')
            users = request.POST.getlist('users')
            if len(users):
                case = self.get_object()
                case.share(request.user, users, message, request.is_secure())
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
