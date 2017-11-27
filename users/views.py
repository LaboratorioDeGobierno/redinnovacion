# -*- coding: utf-8 -*-

# forms
from users.forms import AuthenticationForm
from users.forms import CaptchaAuthenticationForm
from users.forms import UserCreationCompleteForm
from users.forms import UserCreationForm
from users.forms import UserInstitutionCreationForm
from users.forms import UserForm
from users.forms import UserPasswordForm
from users.forms import UserProfileForm
from users.forms import UserImageForm
from users.resources import ExportUserResource

# models
from institutions.models import Institution
from regions.models import Region
from users.models import User, UserProfile

# django
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout as django_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import login as django_login_view
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.http import base36_to_int
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import RedirectView
from django.views.generic import TemplateView

# views
from base.views import BaseCreateView
from base.views import BaseListView, BaseUpdateView, BaseDetailView
from base.views import BaseSubModelCreateView
from base.views import export_to_excel

# mixins

from regions.mixins import UserRegionMixin
from users.mixins import TopActiveUsersMixin


def login(request):

    """ view that renders the login """

    if request.user.is_authenticated():
        return redirect('home')

    def captched_form(req=None, data=None):
        return CaptchaAuthenticationForm(
            req, data, initial={'captcha': request.META['REMOTE_ADDR']})

    template_name = "accounts/login.jade"

    login_try_count = request.session.get('login_try_count', 0)

    # If the form has been submitted...
    if request.method == "POST":
        request.session['login_try_count'] = login_try_count + 1

    if login_try_count >= 20:
        return django_login_view(request, authentication_form=captched_form,
                                 template_name=template_name)

    return django_login_view(request, authentication_form=AuthenticationForm,
                             template_name=template_name)


def logout(request):
    """ view that handles the logout """
    django_logout(request)
    return redirect('home')


@login_required
def password_change(request):
    """ view that renders the login """
    # If the form has been submitted...
    template_name = "accounts/password_change.jade"

    return auth_views.password_change(request, post_change_redirect="/",
                                      template_name=template_name)


def password_reset(request):
    """ view that handles the recover password process """
    success_url = reverse('password_email_sent')
    template_name = 'accounts/password_reset_form.jade'

    if request.method == "POST":
        if request.POST.get('email'):
            email = request.POST.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                if user.status == User.STATUS_PENDING:
                    msg = AuthenticationForm.error_messages['pending']
                    messages.add_message(request, messages.INFO, msg)
                if not user.is_active or user.status != User.STATUS_ACCEPTED:
                    msg = u'Este email no de un miembro de la red'
                    messages.add_message(request, messages.ERROR, msg)
                    return redirect('home')
            else:
                msg = u'El email no está registrado en nuestra base de datos'
                messages.add_message(request, messages.ERROR, msg)
                return redirect('home')
            user.send_recover_password_email(request)
        return redirect(success_url)

    return auth_views.password_reset(
        request,
        template_name=template_name,
        post_reset_redirect=success_url,
    )


def password_reset_email_sent(request):
    messages.add_message(request, messages.INFO,
                         _("An email has been sent to you. Please check it "
                           "to reset your password."))
    return redirect('home')


def password_reset_confirm(request, uidb64, token):
    """ view that handles the recover password process """
    template_name = "registration/password_reset_confirm.jade"
    success_url = "/accounts/reset/done/"

    return auth_views.password_reset_confirm(request, uidb64, token,
                                             template_name=template_name,
                                             post_reset_redirect=success_url)


def password_reset_complete(request):
    """ view that handles the recover password process """

    template_name = "registration/password_reset_complete.jade"
    return auth_views.password_reset_complete(request,
                                              template_name=template_name)


class UserCreateView(BaseCreateView):
    model = User
    template_name = 'accounts/create.jade'
    form_class = UserCreationForm
    navbar_active = 'participants'


class InstitutionUserCreateView(BaseSubModelCreateView):
    model = User
    parent_model = Institution
    template_name = 'accounts/create.jade'
    form_class = UserInstitutionCreationForm
    navbar_active = 'participants'


class RegisterView(BaseCreateView):
    template_name = 'accounts/user_new.jade'
    form_class = UserCreationCompleteForm
    navbar_active = 'participants'

    def dispatch(self, *args, **kwargs):
        # skip login required
        return super(BaseCreateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('register_success')

    def form_invalid(self, form):
        user = User.objects.filter(email=form.data['email']).first()

        if user and user.status == User.STATUS_OTHER:
            for attr, value in form.cleaned_data.iteritems():
                setattr(user, attr, value)
            user.status = User.STATUS_PENDING
            user.is_active = False
            user.save()
            return redirect('register_success')

        return super(RegisterView, self).form_invalid(form)

    def form_valid(self, form):
        form.cleaned_data['is_active'] = False
        form.cleaned_data['status'] = User.STATUS_PENDING
        return super(RegisterView, self).form_valid(form)


class RegisterSuccessView(TemplateView):
    template_name = 'accounts/register_success.jade'
    navbar_active = 'participants'


class UserEditImageView(BaseUpdateView):
    model = User
    template_name = 'accounts/edit.jade'
    form_class = UserImageForm
    pk_url_kwarg = 'user_pk'
    navbar_active = 'participants'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        super(UserEditImageView, self).dispatch(*args, **kwargs)
        return redirect('user_update')


@login_required
def send_message(request, user_pk):
    body = request.POST.get('body', '')
    subject = request.POST.get('subject', '')
    participant = User.objects.get(pk=user_pk)

    participant.send_email_message(
        request, subject=subject,
        message=body,
    )

    return redirect(participant.get_message_url())


@login_required
def deactivate(request, user_pk):
    # check permission
    if request.user.id != int(user_pk):
        if not request.user.is_staff:
            return redirect('participant_list')

    user_active = User.objects.get(pk=user_pk)

    user_active.is_active = False
    user_active.status = User.STATUS_REJECTED
    user_active.save()

    user_active.force_logout()

    if request.user.pk == user_pk:
        messages.add_message(
            request, messages.INFO,
            _("La cuenta fue eliminada")
        )
        return redirect('home')
    else:
        messages.add_message(
            request, messages.INFO,
            _("La cuenta fue desactivada")
        )
        return redirect('rejected_participant_list')


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def user_new_confirm(request, uidb36=None, token=None,
                     token_generator=default_token_generator,
                     current_app=None, extra_context=None):
    """
    View that checks the hash in a email confirmation link and activates
    the user.
    """

    assert uidb36 is not None and token is not None  # checked by URLconf
    try:
        uid_int = base36_to_int(uidb36)
        user = User.objects.get(id=uid_int)
    except (ValueError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.update(is_active=True)
        messages.add_message(request, messages.INFO,
                             _("Your email address has been verified."))
    else:
        messages.add_message(request, messages.ERROR,
                             _("Invalid verification link"))

    return redirect('login')


class BaseUserListView(BaseListView):
    model = User
    navbar_active = 'participants'

    def get_queryset(self):
        query_text = self.request.GET.get('q')
        queryset = super(BaseUserListView, self).get_queryset()
        if query_text:
            for query in query_text.split():
                queryset = queryset.filter(
                    Q(first_name__unaccent__icontains=query) |
                    Q(last_name__unaccent__icontains=query) |
                    Q(mother_family_name__unaccent__icontains=query) |
                    Q(email__icontains=query) |
                    Q(institution__name__unaccent__icontains=query) |
                    Q(region__name__unaccent__icontains=query) |
                    Q(region__short_name__unaccent__icontains=query),
                )
        queryset = queryset.order_by('first_name', 'last_name')
        return queryset

    def get_paginate_by(self, queryset):
        try:
            page = int(self.request.GET.get('by'))
        except:
            page = self.paginate_by
        return page

    def get_context_data(self, **kwargs):
        context = super(BaseUserListView, self).get_context_data(**kwargs)
        page = self.request.GET.get('by')
        try:
            context['by'] = int(page)
        except:
            context['by'] = self.paginate_by
        return context


class ParticipantListView(BaseUserListView):
    template_name = 'participants/participant_list.jade'

    def get_queryset(self):
        queryset = super(ParticipantListView, self).get_queryset()
        queryset = queryset.filter(
            status=User.STATUS_ACCEPTED,
            is_active=True,
        )
        return queryset


class PendingParticipantListView(BaseUserListView):
    template_name = 'participants/pending_participant_list.jade'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_staff:
            redirect('people_list')
        base_user_list = super(PendingParticipantListView, self)
        return base_user_list.dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(PendingParticipantListView, self).get_queryset()
        queryset = queryset.filter(status=User.STATUS_PENDING)
        return queryset


class RejectedParticipantListView(BaseUserListView):
    template_name = 'participants/rejected_participant_list.jade'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_staff:
            redirect('people_list')
        base_user_list = super(RejectedParticipantListView, self)
        return base_user_list.dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(RejectedParticipantListView, self).get_queryset()
        queryset = queryset.filter(status=User.STATUS_REJECTED)
        return queryset


class ExternParticipantListView(BaseUserListView):
    template_name = 'participants/extern_participant_list.jade'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_staff:
            redirect('people_list')
        base_user_list = super(ExternParticipantListView, self)
        return base_user_list.dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(ExternParticipantListView, self).get_queryset()
        queryset = queryset.filter(
            status=User.STATUS_ACCEPTED,
            is_active=False,
        )
        return queryset


class StatusUserRedirectView(RedirectView):
    permanent = False
    pattern_name = 'participant_list'
    is_active = None
    is_staff = None

    @method_decorator(staff_member_required)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StatusUserRedirectView, self).dispatch(*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        self.change_status(kwargs['user_pk'])
        return reverse(self.pattern_name)

    def change_status(self, user_pk):
        user = get_object_or_404(User, pk=user_pk)

        # update is active attribute
        if self.is_active is not None:
            user.is_active = self.is_active

        # update is staff attribute
        if self.is_staff is not None:
            user.is_staff = self.is_staff
            user.is_superuser = self.is_staff

        # update status and store a copy of the previous status
        old_status = user.status
        user.status = self.status
        user.save()

        # if the user is now accpted but previously he was not accepted
        if self.status == User.STATUS_ACCEPTED and old_status != self.status:
            # send the activate email
            user.send_activate_email(self.request)

        if self.status == User.STATUS_REJECTED and old_status != self.status:
            # send the activate email
            user.send_rejection_email(self.request)

        if user.is_active:
            kind = 'Funcionario'
        else:
            kind = 'Externo'

        if user.is_staff:
            staff_status = '(STAFF)'
        else:
            staff_status = ''

        messages.add_message(
            self.request,
            messages.SUCCESS,
            u"El estado del {} fue actualizado a: {} - {} {}".format(
                user.get_full_name(),
                user.get_status_display(),
                kind,
                staff_status,
            ),
        )


class AcceptUserRedirectView(StatusUserRedirectView):
    pattern_name = 'pending_participant_list'
    status = User.STATUS_ACCEPTED
    is_active = True
    is_staff = False


class AcceptStaffUserRedirectView(StatusUserRedirectView):
    pattern_name = 'pending_participant_list'
    status = User.STATUS_ACCEPTED
    is_active = True
    is_staff = True


class RemoveStaffUserRedirectView(StatusUserRedirectView):
    pattern_name = 'user_admin_list_view'
    status = User.STATUS_ACCEPTED
    is_active = True
    is_staff = False


class AcceptExternUserRedirectView(StatusUserRedirectView):
    pattern_name = 'pending_participant_list'
    status = User.STATUS_ACCEPTED
    is_active = False


class RejectUserRedirectView(StatusUserRedirectView):
    status = User.STATUS_REJECTED
    is_active = False


class DeleteAccountRedirectView(RedirectView):
    permanent = False
    pattern_name = 'home'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(
            DeleteAccountRedirectView, self).dispatch(*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        self.desactive_user(kwargs['user_pk'])
        return reverse(self.pattern_name)

    def desactive_user(self, user_pk):
        if int(self.request.user.pk) == int(user_pk):
            user = get_object_or_404(User, pk=user_pk)
            user.is_active = False
            user.status = User.STATUS_REJECTED
            user.save()
            user.force_logout()


class ParticipantDetailView(BaseDetailView):
    model = User
    template_name = 'participants/participant_detail.jade'
    context_object_name = 'participant'
    navbar_active = 'participants'

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        slug = self.kwargs.get(self.slug_url_kwarg, None)

        if pk is None and slug is None:
            return self.request.user

        return super(ParticipantDetailView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(ParticipantDetailView, self).get_context_data(**kwargs)
        #
        participant = context['participant']

        # get recent email messages
        context['senders'] = User.objects.filter(
            id__in=participant.received_email_messages.values(
                'from_user_id'
            )[:5]
        )

        context['my_pending_activities'] = participant.useractivity_set.filter(
            attendance_date__isnull=True,
            activity__event__start_date__gte=timezone.now(),
        ).order_by('activity__event__start_date')[:3]

        context['past_activities'] = participant.useractivity_set.filter(
            attendance_date__isnull=True,
            activity__event__start_date__lte=timezone.now(),
        ).order_by('activity__event__start_date')[:3]

        # comments
        context['comments'] = participant.comment_set.base_comments()[:10]

        return context


class ParticipantUserUpdateView(BaseUpdateView):
    model = User
    template_name = 'participants/admin_user_update.jade'
    context_object_name = 'participant'
    form_class = UserForm
    active_tab = 'profile'
    form_template = 'includes/participant_form.jade'
    navbar_active = 'participants'

    def get_context_data(self, **kwargs):
        cast = super(ParticipantUserUpdateView, self)
        context = cast.get_context_data(**kwargs)
        context['active_tab'] = self.active_tab
        context['form_template'] = self.form_template
        return context

    @method_decorator(staff_member_required)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        base_update_view = super(ParticipantUserUpdateView, self)
        return base_update_view.dispatch(*args, **kwargs)


class ParticipantProfileUpdateView(ParticipantUserUpdateView):
    model = User
    form_class = UserProfileForm
    active_tab = 'privacy'
    form_template = 'includes/profile_form.jade'

    def get_form_kwargs(self):
        kwargs = super(ParticipantProfileUpdateView, self).get_form_kwargs()
        profile = getattr(self.object, 'profile', None)

        if profile is None:
            profile = UserProfile.objects.create(user=self.object)

        kwargs['instance'] = profile
        return kwargs


class ParticipantPasswordUpdateView(ParticipantUserUpdateView):
    form_class = UserPasswordForm
    active_tab = 'password'
    form_template = 'includes/password_form.jade'


class ParticipantAvatarUpdateView(ParticipantUserUpdateView):
    active_tab = 'avatar'
    form_template = 'includes/avatar_form.jade'


class ParticipantAccountUpdateView(ParticipantUserUpdateView):
    active_tab = 'account'
    form_template = 'includes/account_form.jade'


class UserUpdateView(BaseUpdateView):
    model = User
    template_name = 'accounts/edit.jade'
    context_object_name = 'participant'
    form_class = UserForm
    active_tab = 'profile'
    form_template = 'includes/participant_form.jade'
    navbar_active = 'participants'

    def get_context_data(self, **kwargs):
        cast = super(UserUpdateView, self)
        context = cast.get_context_data(**kwargs)
        context['active_tab'] = self.active_tab
        context['form_template'] = self.form_template
        return context

    def get_object(self, queryset=None):
        self.object = self.request.user
        return self.object

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        base_update_view = super(UserUpdateView, self)
        return base_update_view.dispatch(*args, **kwargs)


class UserProfileUpdateView(UserUpdateView):
    model = UserProfile
    form_class = UserProfileForm
    active_tab = 'privacy'
    form_template = 'includes/profile_form.jade'

    def get_object(self, queryset=None):
        super(UserProfileUpdateView, self).get_object(queryset)
        profile = getattr(self.object, 'profile', None)
        if profile is None:
            profile = UserProfile.objects.create(user=self.object)
        self.object = profile
        return self.object


class UserPasswordUpdateView(UserUpdateView):
    form_class = UserPasswordForm
    active_tab = 'password'
    form_template = 'includes/password_form.jade'

    def form_valid(self, form):
        response = super(UserPasswordUpdateView, self).form_valid(form)
        update_session_auth_hash(self.request, form.instance)
        return response


class UserAvatarUpdateView(UserUpdateView):
    active_tab = 'avatar'
    form_template = 'includes/avatar_form.jade'


class UserAccountUpdateView(UserUpdateView):
    active_tab = 'account'
    form_template = 'includes/account_form.jade'


class UserAdminListView(BaseListView):
    model = User
    template_name = 'participants/admin_user_list.jade'
    navbar_active = 'participants'

    @method_decorator(staff_member_required)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserAdminListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(UserAdminListView, self).get_queryset()
        queryset = queryset.filter(is_staff=True, is_active=True)
        queryset = queryset.order_by('first_name', 'last_name')
        return queryset


class DeleteAddAdminBaseRedirectView(RedirectView):
    permanent = False
    pattern_name = 'user_admin_list_view'

    @method_decorator(staff_member_required)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(
            DeleteAddAdminBaseRedirectView, self).dispatch(*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        user_pk = kwargs['user_pk']
        if not int(self.request.user.pk) == int(user_pk):
            self.change_is_staff(kwargs['user_pk'])
        return reverse(self.pattern_name)

    def change_is_staff(self, user_pk):
        user = get_object_or_404(User, pk=user_pk)
        user.is_staff = self.is_staff
        user.save()


class AddAdminRedirectView(DeleteAddAdminBaseRedirectView):
    is_staff = True


class DeleteAdminRedirectView(DeleteAddAdminBaseRedirectView):
    is_staff = False


def export_users(request):
    if not request.user.is_member():
        raise Http404

    filters = {}
    for key in request.GET:
        value = request.GET.get(key)
        if value:
            try:
                value = int(value)
            except TypeError:
                pass
            filters[key] = value

    # region parameter is region order
    if 'region' in filters:
        filters['region__order'] = filters.pop('region')

    queryset = User.objects.members().filter(**filters)
    return export_to_excel(
        request,
        resource_class=ExportUserResource,
        queryset=queryset,
    )


@login_required
@staff_member_required
def send_recover_password_email(request, user_pk):
    """
    Sends an email to the user indicated in the url with instructions to
    recover their password
    """
    user = get_object_or_404(User, pk=user_pk)
    user.send_recover_password_email(request)
    messages.add_message(
        request, messages.SUCCESS, _('email sent').capitalize()
    )
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def terms(request):
    """ view that renders the terms """
    template_name = "accounts/terms.jade"

    return render(request, template_name)


def whats(request):
    """ view that renders the whats """
    template_name = "accounts/whats.jade"

    return render(request, template_name)


class PeopleListView(
    BaseUserListView,
    UserRegionMixin,
    TopActiveUsersMixin,
):
    template_name = 'activity/most_active_users.jade'

    def get_queryset(self):
        queryset = super(PeopleListView, self).get_queryset()
        queryset = queryset.select_related(
            'institution',
            'region',
        ).prefetch_related(
            'comment_set',
            'useractivity_set',
        ).filter(
            status=User.STATUS_ACCEPTED,
            is_active=True,
        )
        region_order = self.request.GET.get('region')
        if region_order:
            queryset = queryset.filter(region__order=region_order)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(PeopleListView, self).get_context_data(**kwargs)

        region_order = self.request.GET.get('region')

        if region_order:
            context['current_region'] = Region.objects.get(order=region_order)
        else:
            context['current_region'] = u'Todos los usuarios de la Red'

        return context
