from base.mockups import Mockup
from notifications.enums import NotificationKinds
from users.models import User

from django.utils import timezone


def create_notifications(user=None):
    m = Mockup()

    if user is None:
        user = User.objects.order_by('-last_activity').first()

    event = m.create_event(start_date=timezone.now())

    for kind, name in NotificationKinds.choices:
        m.create_notification(
            user=user,
            kind=kind,
            event=event,
            comment=m.create_comment(event=event),
            from_user=m.create_user(),
        )


def create_admin_user():
    m = Mockup()
    user = m.get_or_create_user(email='admin@admin.com')[0]
    user.set_password('admin')
    user.is_staff = True
    user.is_active = True
    user.is_superuser = True
    user.status = user.STATUS_ACCEPTED
    user.save()
    return user
