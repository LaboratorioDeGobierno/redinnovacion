# -*- coding: utf-8 -*-
""" Views for the dynamic_contents application. """
# standard library

# django
from django.core.urlresolvers import reverse

# models
from .models import DynamicContent
from documentation.models import Methodology
from documentation.models import Tool
from cases.models import Case

# views
from base.views import BaseCreateView
from base.views import BaseDeleteView
from base.views import BaseDetailView
from base.views import BaseListView
from base.views import BaseUpdateView

# forms
from .forms import DynamicContentForm


class DynamicContentListView(BaseListView):
    """
    View for displaying a list of dynamic_contents.
    """
    model = DynamicContent
    template_name = 'dynamic_contents/dynamic_content_list.jade'
    permission_required = 'dynamic_contents.view_dynamic_content'


class DynamicContentCreateView(BaseCreateView):
    """
    A view for creating a single dynamic_content
    """
    model = DynamicContent
    form_class = DynamicContentForm
    template_name = 'dynamic_contents/dynamic_content_create.jade'
    permission_required = 'dynamic_contents.add_dynamic_content'

    def get_form(self, form_class=None):
        """
        Returns an instance of the form to be used in this view.
        """
        form = super(DynamicContentCreateView, self).get_form(form_class)

        form.instance.created_by = self.request.user

        self.methodology = None
        self.tool = None
        self.case = None

        if 'methodology_pk' in self.kwargs:
            self.methodology = Methodology.objects.get(
                pk=self.kwargs['methodology_pk']
            )

        if 'tool_pk' in self.kwargs:
            self.tool = Tool.objects.get(
                pk=self.kwargs['tool_pk']
            )

        if 'case_pk' in self.kwargs:
            self.case = Case.objects.get(
                pk=self.kwargs['case_pk']
            )

        form.instance.methodology = self.methodology
        form.instance.tool = self.tool
        form.instance.case = self.case

        self.form = form

        return form

    def get_success_url(self):
        if (self.object.kind == self.object.GALLERY or
                self.object.kind == self.object.IMAGE):
            return reverse('dynamic_content_update', args=(self.object.id,))
        return super(DynamicContentCreateView, self).get_success_url()

    def get_context_data(self, **kwargs):
        context = super(DynamicContentCreateView, self).get_context_data(
            **kwargs
        )

        context['cancel_url'] = self.form.instance.get_absolute_url()

        return context


class DynamicContentDetailView(BaseDetailView):
    """
    A view for displaying a single dynamic_content
    """
    model = DynamicContent
    template_name = 'documentation/includes/single_dynamic_content.jade'
    permission_required = 'dynamic_contents.view_dynamic_content'

    def get_context_data(self, **kwargs):
        context = super(DynamicContentDetailView, self).get_context_data(
            **kwargs
        )

        context['dynamic_content'] = self.object
        context['readonly'] = True

        return context


class DynamicContentUpdateView(BaseUpdateView):
    """
    A view for editing a single dynamic_content
    """
    model = DynamicContent
    form_class = DynamicContentForm
    template_name = 'dynamic_contents/dynamic_content_update.jade'
    permission_required = 'dynamic_contents.change_dynamic_content'

    def get_object(self):
        self.object = super(DynamicContentUpdateView, self).get_object()
        self.original_order = self.object.order

        return self.object

    def form_valid(self, form):

        response = super(DynamicContentUpdateView, self).form_valid(form)

        # use replace order function, requires old order set
        if self.object.order != self.original_order:
            new_order = self.object.order
            self.object.order = self.original_order
            self.object.replace_order(new_order)

        return response


class DynamicContentDeleteView(BaseDeleteView):
    """
    A view for deleting a single dynamic_content
    """
    model = DynamicContent
    permission_required = 'dynamic_contents.delete_dynamic_content'
    template_name = 'dynamic_contents/dynamic_content_delete.jade'

    def get_success_url(self):
        return self.object.get_absolute_url()
