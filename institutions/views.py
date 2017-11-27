from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView

from base import views
from institutions.models import Institution
from institutions.models import InstitutionKind
from institutions.forms import InstitutionForm
from users.models import User


class InstitutionListView(views.BaseListView):
    model = Institution
    template_name = 'institutions/institution_list.jade'
    queryset = Institution.objects.active()
    navbar_active = 'participants'

    def get_template_names(self):
        template_names = super(
            InstitutionListView,
            self).get_template_names()
        if self.request.user.is_staff:
            template_names.insert(
                0,
                'institutions/admin_institution_list.jade'
            )
        return template_names

    def get_queryset(self):
        queryset = super(InstitutionListView, self).get_queryset()

        if not self.request.user.is_staff:
            queryset = queryset.annotate(user_count=Count('users'))
            queryset = queryset.filter(user_count__gt=0)

        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(name__unaccent__icontains=query)
        return queryset


class InstitutionCreateView(views.CreateView):
    model = Institution
    form_class = InstitutionForm
    template_name = 'institutions/institution_create.jade'
    permission_required = 'add_institution'
    navbar_active = 'participants'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InstitutionCreateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return self.object.get_absolute_url()


class InstitutionDetailView(views.BaseDetailView):
    model = Institution
    context_object_name = 'institution'
    queryset = Institution.objects.all()
    template_name = 'institutions/institution_detail.jade'
    navbar_active = 'participants'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InstitutionDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InstitutionDetailView, self).get_context_data(**kwargs)
        context['user_list'] = self.object.users.filter(
            status=User.STATUS_ACCEPTED
        )
        return context

    def render_to_response(self, context, **kwargs):
        if self.request.user.is_staff:
            return redirect('institution_update', self.object.slug)
        super_obj = super(InstitutionDetailView, self)
        return super_obj.render_to_response(context, **kwargs)


class InstitutionUpdateView(views.BaseUpdateView):
    model = Institution
    form_class = InstitutionForm
    slug_url_kwarg = 'slug'
    template_name = 'institutions/institution_update.jade'
    navbar_active = 'participants'

    @method_decorator(staff_member_required)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InstitutionUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InstitutionUpdateView, self).get_context_data(**kwargs)
        context['user_list'] = self.get_users()
        return context

    def get_users(self):
        user_list = self.object.users.filter(is_active=True)
        paginator = Paginator(user_list, views.PAGINATE_BY)
        page = self.request.GET.get(views.PAGE_KWARG)

        try:
            users = paginator.page(page)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        except:
            users = paginator.page(1)
        return users


class InstitutionDeleteView(RedirectView):
    model = Institution
    pattern_name = 'institution_list'
    permanent = False

    @method_decorator(staff_member_required)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InstitutionDeleteView, self).dispatch(*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        self.delete_institution(kwargs['slug'])
        return reverse(self.pattern_name)

    def delete_institution(self, slug):
        institution = get_object_or_404(Institution, slug=slug)
        institution.is_active = False
        institution.save()


class InstitutionMostActiveListView(views.BaseListView):
    model = Institution
    template_name = 'institutions/most_active_institutions.jade'
    queryset = Institution.objects.active()
    navbar_active = 'participants'
    ordering = '-num_users'

    def get_ordering(self):
        """
        Return the field or fields to use for ordering the queryset.
        """
        self.ordering = self.request.GET.get('order', self.ordering)
        return self.ordering

    def get_queryset(self):
        queryset = super(InstitutionMostActiveListView, self).get_queryset()

        self.institution_kind = self.request.GET.get('institution_kind')

        queryset = queryset.annotate(num_users=Count('users'))
        queryset = queryset.filter(num_users__gt=0)

        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(name__unaccent__icontains=query)

        self.all_institutions = queryset

        if self.institution_kind:
            queryset = queryset.filter(kind_id=self.institution_kind)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(InstitutionMostActiveListView, self).get_context_data(
            **kwargs
        )

        types = Institution.report_by_kind()

        if self.institution_kind:
            current_institution_kind = InstitutionKind.objects.filter(
                pk=self.institution_kind
            ).first().name
        else:
            current_institution_kind = 'Todas las instituciones'

        context.update({
            'institution_types': types,
            'institutions': self.all_institutions,
            'current_institution': current_institution_kind,
            'by': self.paginate_by,
            'ordering': self.ordering,
        })
        return context
