from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from base.views import BaseListView

from users.models import User


class AdminListView(BaseListView):
    model = User
    template_name = 'configs/admin_list.jade'

    @method_decorator(staff_member_required)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(
            AdminListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(
            AdminListView, self).get_queryset()
        return queryset.filter(
            is_staff=True).exclude(is_superuser=True)


class AdminDeleteRedirectView(RedirectView):
    permanent = False
    pattern_name = 'admin_list_view'

    @method_decorator(staff_member_required)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(
            AdminDeleteRedirectView, self).dispatch(*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        user_pk = kwargs['user_pk']
        user = get_object_or_404(User, pk=user_pk)
        user.is_staff = False
        user.save()
        return reverse(self.pattern_name)
