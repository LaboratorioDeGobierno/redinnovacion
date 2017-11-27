# django
from django.views.generic.base import ContextMixin

# models
from regions.models import Region


class UserRegionMixin(ContextMixin):
    """
    Add users by region to the context
    """
    def get_context_data(self, **kwargs):
        ctx = super(UserRegionMixin, self).get_context_data(**kwargs)
        regions = Region.get_user_count_by_region()
        ctx['regions'] = regions
        ctx['total_users'] = sum(
            [region['users__count'] for region in regions]
        )
        return ctx
