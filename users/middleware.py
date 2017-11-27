# django
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils import timezone


class UpdateLastActivityMiddleware(object):
    """
    UpdateLastActivityMiddleware saves the last action performed by the user
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        # check if auth middleware is installed
        assert hasattr(request, 'user'), 'Requires authentication middleware.'
        # if user is logged, save timestamp
        if request.user.is_authenticated():
            request.user.update(last_activity=timezone.now())


class PendingUserMiddleware(object):
    """
    PendingUserMiddleware redirects to home if the user is a PENDING user
    """
    def process_request(self, request):
        if settings.TEST:
            return

        if not request.user.is_authenticated():
            return
        # accepted paths
        accept_path = (
            request.path == '/'
            or request.path.startswith('/api/')
            or request.path.startswith('/accounts/logout')
            or request.path.startswith('/admin/logout')
            or request.path.startswith('/dist/')
            or request.path.startswith('/uploads/')
            or request.path.startswith('/static/')
            or request.path.startswith('/notifications/last')
        )
        if not accept_path and request.user.is_pending():
            return redirect(reverse('home'))
