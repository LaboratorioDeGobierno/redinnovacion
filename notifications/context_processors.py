
# django

# models
from .models import Notification

# views

# forms


def current_notifications(request):
    if not request.user.is_authenticated():
        return {}

    context = {}

    # get unread notifications: read=False
    unread_notifications = request.user.notification_set.filter(
        read=False
    )

    # add unread notifications count to the context
    context['unread_notifications'] = (
        unread_notifications.count()
    )

    # get unread messages: read=False
    unread_messages = request.user.received_email_messages.filter(
        read=False
    )

    # add unread messages count to the context
    context['unread_messages'] = (
        unread_messages.count()
    )

    # get last messages notifications: (id, sender)
    unread_notifications_messages_ids_by_sender = (
        request.user.notification_set.filter(
            email_message__in=unread_messages
        ).values_list('id', 'from_user').order_by('-id')
    )

    # saves messages ids
    unread_notifications_messages_ids = []

    # save unique senders
    senders = []

    # add unique sender with his messages id
    for pk, sender in unread_notifications_messages_ids_by_sender:
        if sender and sender not in senders:
            senders.append(sender)
            unread_notifications_messages_ids.append(pk)

    # merge notifications
    user_notifications = request.user.notification_set.filter(
        id__in=(
            list(unread_notifications.values_list('id', flat=True))
            + list(unread_notifications_messages_ids)
        )
    ).distinct()

    # get first 10 notifications
    user_notifications = list(
        user_notifications.order_by('-updated_at')[:10]
    )

    # add first 10 notifications to the context
    context['dropdown_notifications_list'] = user_notifications

    # add total notifications to the context
    context['total_notifications'] = (
        context['unread_notifications'] + context['unread_messages']
    )
    return context
