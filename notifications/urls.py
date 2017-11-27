from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.NotificationListView.as_view(),
        name='notification_list'
    ),
    url(
        r'^last/$',
        views.LastNotificationView.as_view(),
        name='last_notifications'
    ),
]
