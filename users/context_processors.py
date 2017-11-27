# django
from django.utils import timezone

# models
from users.models import User

# date
from datetime import timedelta

# enums
from users.enums import UserEnum


def active_users(request):
    """
    Add active users to the context
    """
    if not request.user.is_authenticated():
        return {}

    timestamp = timezone.now() - timedelta(minutes=5)
    users = User.objects.filter(
        is_active=True,
        status=UserEnum.STATUS_ACCEPTED,
        last_activity__gte=timestamp
    ).exclude(pk=request.user.pk)

    context = {
        'active_users': users,
    }

    return context
