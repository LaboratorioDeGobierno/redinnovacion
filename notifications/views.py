# -*- coding: utf-8 -*-
""" Views for the notifications application. """
# standard library

# django
from django.views.generic.base import TemplateView

# models
from .models import Notification

# views
from base.views import BaseListView

# forms


class NotificationListView(BaseListView):
    """
    View for displaying a list of notifications.
    """
    model = Notification
    template_name = 'notifications/list.jade'
    ordering = ('-id',)

    def get_queryset(self):
        queryset = super(NotificationListView, self).get_queryset()

        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(NotificationListView, self).get_context_data(**kwargs)

        notification_ids = []
        for notification in context['object_list']:
            notification_ids.append(notification.id)

        # Get the unread notification list
        unread_notifications = self.request.user.notification_set.filter(
            read=False
        )
        # replace the unread notifications since we are marking them as read
        context['unread_notifications'] = unread_notifications.count()
        context['dropdown_notifications_list'] = list(
            unread_notifications.order_by('-created_at')[:10]
        )

        context['body_class'] = 'notifications-list'

        Notification.objects.filter(id__in=notification_ids).update(read=True)

        return context


class LastNotificationView(TemplateView):

    template_name = "notifications/includes/dropdown.jade"

    def get_context_data(self, **kwargs):
        context = super(LastNotificationView, self).get_context_data(**kwargs)

        # anon users doesn't need this data
        if (
            not self.request.user.is_authenticated()
            or self.request.user.is_pending()
        ):
            return {}

        # get unread notifications
        unread_notifications = self.request.user.notification_set.filter(
            read=False
        )
        # add unread notifications count to the context
        context['unread_notifications'] = unread_notifications.count()

        # get unread messages
        unread_messages = self.request.user.received_email_messages.filter(
            read=False
        )
        # add unread messages count to the context
        context['unread_messages'] = unread_messages.count()

        # get messages notifications
        unread_notifications_messages_ids = (
            self.request.user.notification_set.filter(
                email_message__in=unread_messages
                ).values_list('id', flat=True)
        )

        user_notifications = self.request.user.notification_set.filter(
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
        context['dropdown_notifications_list'] = user_notifications[:10]

        # add total notifications count to the context
        context['total_notifications'] = (
            context['unread_notifications'] + context['unread_messages']
        )

        return context
