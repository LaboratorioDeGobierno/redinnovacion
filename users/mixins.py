# django
from django.views.generic.base import ContextMixin

# models
from users.models import User


class TopActiveUsersMixin(ContextMixin):
    """
    Add top 3 active users to the context
    """
    def get_context_data(self, **kwargs):
        ctx = super(TopActiveUsersMixin, self).get_context_data(**kwargs)
        ctx['top_users'] = User.objects.top_active_users()
        return ctx
