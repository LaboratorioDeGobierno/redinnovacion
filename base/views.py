# -*- coding: utf-8 -*-
""" This file contains some generic purpouse views """

# standard library
import os

# excel import
import tablib

# django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.base import ContextMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django_pdfkit import PDFView

# utils
from base.utils import camel_to_underscore
from base.utils import today
from base.view_utils import clean_query_string
from base.view_utils import render_to_json_response
import pdfkit

# models
from events.models import Event
from events.models import Stage
from comments.models import Comment
from institutions.models import Institution
from regions.models import Region

# forms
from comments.forms import CommentForm

# import export
from import_export.formats import base_formats

# magic
import magic

PAGINATE_BY = 25
PAGE_KWARG = 'p'


@login_required
def index(request, disqus=False, comment_id=None):
    """ view that renders a default home"""
    user = request.user
    activities = user.useractivity_set.prefetch_related('activity__event')
    my_pending_activities = activities.filter(
        attendance_date__isnull=True,
        activity__event__start_date__gte=today(),
    )[:3]
    incomming_events = Event.objects.incomming().filter(
        stage__stage_type=Stage.STAGE_TYPE_ACTIVITY,
        stage__is_active=True,
    )

    comments = Comment.objects.filter(parent=None, public=True)

    if not request.user.is_experimenta():
        incomming_events = incomming_events.exclude(
            activity_type=Event.ACTIVITY_TYPES.EXPERIMENTA
        )
        comments = comments.exclude(
            event__activity_type=Event.ACTIVITY_TYPES.EXPERIMENTA
        )

    incomming_events = incomming_events[:5]

    if comment_id:
        comment = comments.filter(id=comment_id).first()
        # marks the children of the comment as read
        for c in comment.comment_set.all():
            c.notification_set.all().update(read=True)

        comments = list(comments.exclude(id=comment_id)[:9])

        if comment:
            comments.insert(0, comment)
    else:
        comments = list(comments[:10])

    # get users by region
    regions = Region.get_user_count_by_region()
    # get info about total_users except top 3
    others = {
        'users__count': sum([o['users__count'] for o in regions[3:]]),
        'percent': 100-sum([region['percent'] for region in regions[:3]])
    }
    # total users with region
    total_users = sum([region['users__count'] for region in regions])

    # institutions with users
    institutions_count = Institution.objects.has_users().active().count()

    msg = (
        u"Su cuenta en La Red se encuentra pendiente"
        u" de aprobación. Por lo que no puedes realizar acciones en el"
        u" sitio hasta que sea aprobada."
    )
    if request.user.is_pending():
        messages.add_message(
            request, messages.ERROR,
            msg
        )

    context = {
        'form': CommentForm(),
        'interest_list': request.user.interests.all(),
        'my_pending_activities': my_pending_activities,
        'incomming_events': incomming_events,
        'my_pending_activities': my_pending_activities,
        'comments': comments,
        'navbar_active': 'home',
        'institutions_count': institutions_count,
        'regions': regions,
        'total_users': total_users,
        'others': others,
    }

    return render_to_response(
        'index.jade',
        context,
        context_instance=RequestContext(request),
    )


def bad_request_view(request):
    response = render_to_response('exceptions/400.jade', {},
                                  context_instance=RequestContext(request))
    response.status_code = 400

    return response


def permission_denied_view(request):
    response = render_to_response('exceptions/403.jade', {},
                                  context_instance=RequestContext(request))
    response.status_code = 403

    return response


def page_not_found_view(request):
    response = render_to_response('exceptions/404.jade', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404

    return response


def error_view(request):
    response = render_to_response('exceptions/500.jade', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500

    return response


class PermissionRequiredMixin:
    permission_required = None

    def check_permission_required(self):
        if self.permission_required:
            if not isinstance(self.permission_required, (list, tuple)):
                self.permission_required = (self.permission_required,)
            for perm in self.permission_required:
                if self.request.user.has_perm(perm):
                    return True
            raise PermissionDenied


class NavbarActiveMixin(ContextMixin):
    navbar_active = None

    def get_context_data(self, **kwargs):
        context = super(NavbarActiveMixin, self).get_context_data(**kwargs)
        context['navbar_active'] = self.navbar_active
        return context


# class LoginRequiredMixin(object):

#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class BaseDetailView(DetailView, PermissionRequiredMixin, NavbarActiveMixin):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseDetailView, self).dispatch(*args, **kwargs)


class BaseCreateView(CreateView, PermissionRequiredMixin, NavbarActiveMixin):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseCreateView, self).dispatch(*args, **kwargs)


class BaseSubModelCreateView(CreateView, PermissionRequiredMixin,
                             NavbarActiveMixin):
    """
    Create view when the object is nested within a parent object
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseSubModelCreateView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        model_underscore_name = camel_to_underscore(self.parent_model.__name__)

        try:
            obj = get_object_or_404(
                self.parent_model,
                pk=self.kwargs['{}_id'.format(model_underscore_name)]
            )
        except KeyError:
            obj = get_object_or_404(
                self.parent_model,
                slug=self.kwargs['slug'.format(model_underscore_name)]
            )

        self.parent = obj
        self.object = self.model(**{model_underscore_name: obj})

        return super(BaseSubModelCreateView, self).get_form_kwargs()

    def get_context_data(self, **kwargs):
        context = super(BaseSubModelCreateView, self).get_context_data(
            **kwargs
        )
        model_underscore_name = camel_to_underscore(self.parent_model.__name__)

        context[model_underscore_name] = self.parent

        return context


class BaseListView(ListView, PermissionRequiredMixin, NavbarActiveMixin):
    paginate_by = PAGINATE_BY
    page_kwarg = PAGE_KWARG
    paginate_by = 10

    def get_paginate_by(self, queryset):
        """
        Get the number of items to paginate by, or ``None`` for no pagination.
        """
        self.paginate_by = int(self.request.GET.get('by', self.paginate_by))
        return self.paginate_by

    def get_ordering(self):
        """
        Return the field or fields to use for ordering the queryset.
        """
        order = self.request.GET.get('_o')
        if order:
            return (order,)

        return super(BaseListView, self).get_ordering()

    def get_context_data(self, **kwargs):
        context = super(BaseListView, self).get_context_data(**kwargs)
        context['clean_query_string'] = clean_query_string(self.request)
        context['q'] = self.request.GET.get('q')
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseListView, self).dispatch(*args, **kwargs)


class BaseUpdateView(UpdateView, PermissionRequiredMixin, NavbarActiveMixin):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseUpdateView, self).get_context_data(**kwargs)

        context['cancel_url'] = self.object.get_absolute_url()

        return context


class BaseDeleteView(DeleteView, PermissionRequiredMixin, NavbarActiveMixin):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.check_permission_required()
        return super(BaseDeleteView, self).dispatch(*args, **kwargs)


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(
            LoginRequiredMixin,
            self
        ).dispatch(request, *args, **kwargs)


class MultiUpdateView(BaseUpdateView):
    form_classes = ()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, forms=None, **kwargs):
        if forms is None:
            forms = self.get_forms()
        base_update_view = super(MultiUpdateView, self)
        return base_update_view.get_context_data(forms=forms)

    def get_form_prefix(self, form_class):
        return camel_to_underscore(form_class.__name__)

    def get_forms(self):
        forms = {}
        kwargs = self.get_form_kwargs()
        for form_class in self.form_classes:
            prefix = self.get_form_prefix(form_class)
            kwargs['prefix'] = prefix
            forms[prefix] = form_class(**kwargs)
        return forms

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS,
            u"Datos actualizados"
        )
        if self.request.user.is_staff:
            return reverse('participant_user_update', kwargs={
                'pk': self.object.pk,
            })
        else:
            return reverse('user_update')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        forms = self.get_forms()
        for form in forms.itervalues():
            if form.is_valid():
                fn_name = u'save_%s' % self.get_form_prefix(form.__class__)
                save_form = getattr(self, fn_name, self.save_form)
                save_form(form)
            else:
                context = self.get_context_data(forms=forms)
                return self.render_to_response(context)
        return HttpResponseRedirect(self.get_success_url())

    def save_form(self, form):
        form.save()


# a mixin to add AJAX support to a form
# must be used with an object-based FormView (e.g. CreateView)
class AjaxFormResponseMixin(object):

    def form_invalid(self, form):
        response = {
            'errors': form.errors
        }
        return render_to_json_response(response, status=400)

    def form_valid(self, form):

        # save
        self.object = form.save()

        response = self.object.to_dict()

        # return the context as json
        return render_to_json_response(response)


class BasePDFView(PDFView):
    pdfkit_kwargs = None

    def get_pdfkit_kwargs(self):
        if self.pdfkit_kwargs:
            return self.pdfkit_kwargs
        else:
            return {}

    def render_pdf(self):
        html = self.render_html()

        options = self.get_pdfkit_options()
        if 'debug' in self.request.GET and settings.DEBUG:
            options['debug-javascript'] = 1

        kwargs = self.get_pdfkit_kwargs()
        binpath = os.environ.get('WKHTMLTOPDF_BIN')
        if binpath:
            kwargs['configuration'] = pdfkit.configuration(wkhtmltopdf=binpath)

        return pdfkit.from_string(html, False, options, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(BasePDFView, self).get(request,  *args, **kwargs)


def export_to_excel(request, resource_class, queryset):
    file_format = base_formats.XLSX()
    resource = resource_class()
    data = resource_class().export(queryset)
    export_data = file_format.export_data(data)

    model = resource.Meta.model

    content_type = file_format.get_content_type()

    response = HttpResponse(export_data, content_type=content_type)

    date_str = timezone.localtime(timezone.now()).strftime('%Y-%m-%d')
    filename = "%s-%s.%s" % (model.__name__,
                             date_str,
                             file_format.get_extension())

    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


class BaseAjaxDeleteView(AjaxFormResponseMixin, BaseDeleteView):
    def delete(self, request, *args, **kwargs):
        if not request.is_ajax():
            return super(
                BaseAjaxDeleteView, self).delete(request, *args, **kwargs)
        self.object = self.get_object()
        response = self.object.to_dict()
        self.object.delete()
        return render_to_json_response(response)


def excel_response(filename, headers, rows, description=None):
    """
    Generate an excel response

    filename: String
    headers: Array(String)
    rows: Array(Array(String))
    description: Array(string)

    format:
    description [...] (first rows are description)
    headers [] (name of columns)
    [ row [] ] (dataset)
    """

    content_type = (
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response = HttpResponse(content_type=content_type)
    filename = '{}.xlsx'.format(filename)
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(
        filename)

    dataset = tablib.Dataset()

    if description is not None:
        for d in description:
            dataset.append_separator(d)

    dataset.headers = headers
    for row in rows:
        dataset.append(row)

    response.write(dataset.get_xlsx())

    return response


class DownloadView(View):
    mimetype = None
    extension = None
    filename = None
    use_xsendfile = True

    def get_filename(self):
        return self.filename

    def get_extension(self):
        return self.extension

    def get_mimetype(self):
        with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
            mimetype = m.id_buffer(self.get_object().get_file().read())
        m.close()
        return mimetype

    def get_location(self):
        '''
        Returns the path the file is currently located at.
        Used only if use_xsendfile is True
        '''
        pass

    def get_contents(self):
        '''
        Returns the contents of the file download.
        Used only if use_xsendfile is False
        '''
        pass

    def logging(self):
        """
        Log download
        """
        pass

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type=self.get_mimetype())
        response['Content-Disposition'] = 'filename=' + self.get_filename()

        if self.use_xsendfile is True:
            response['X-Sendfile'] = self.get_location()
        else:
            response.write(self.get_contents().read())
        self.logging()
        return response


class FormsetViewMixin(object):
    formset_class = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        formset = self.get_formset()
        form = self.get_form()
        return self.render_to_response(
            self.get_context_data(formset=formset, form=form)
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = self.get_formset()
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        form_valid = super(FormsetViewMixin, self).form_valid(form)
        formset.instance = self.object
        formset.save()
        return form_valid

    def form_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


class BaseFormsetCreateView(FormsetViewMixin, BaseCreateView):

    def get_object(self, queryset=None):
        return None

    def get_formset(self):
        if self.request.POST:
            formset = self.formset_class(
                self.request.POST,
            )
        else:
            formset = self.formset_class()
        return formset


class BaseFormsetUpdateView(FormsetViewMixin, BaseUpdateView):

    def get_formset(self):
        if self.request.POST:
            formset = self.formset_class(
                self.request.POST,
                instance=self.object,
            )
        else:
            formset = self.formset_class(
                instance=self.object,
            )
        return formset
