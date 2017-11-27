from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^new/$',
        views.CreateEmailMessageCreateView.as_view(),
        name='email_message_list'
    ),
    url(
        r'^$',
        views.EmailMessageListView.as_view(),
        name='email_message_list'
    ),
    url(
        r'^u/(?P<user_pk>[\d]+)/$',
        views.EmailMessageListView.as_view(),
        name='email_message_list_by_pk'
    ),
    url(
        r'^(?P<slug>[\w-]+)/$',
        views.EmailMessageListView.as_view(),
        name='email_message_list'
    ),
]
