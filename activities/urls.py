from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^(?P<pk>\d+)/$',
        views.ActivityDetailView.as_view(),
        name='activity_detail',
    ),
    url(
        r'^(?P<pk>\d+)/participants/$',
        views.ActivityParticipantsView.as_view(),
        name='activity_participants',
    ),
    url(
        r'^(?P<pk>\d+)/participants/excel/$',
        views.ExcelParticipants.as_view(),
        name='excel_activity_participants',
    ),
    url(
        r'^global/participants/excel/$',
        views.ExcelGlobalParticipants.as_view(),
        name='excel_global_participants',
    ),
    url(
        r'^(?P<pk>\d+)/delete/$',
        views.ActivityDeleteView.as_view(),
        name='delete_activity'
    ),
    url(
        r'^(?P<pk>\d+)/certificate/$',
        views.ActivityCertificateView.as_view(),
        name='activity_certificate',
    ),
    url(
        r'^(?P<pk>\d+)/update/$',
        views.ActivityUpdateView.as_view(),
        name='activity_update_view'
    ),
    url(
        r'^(?P<pk>\d+)/inscription/$',
        views.UserActivityCreateView.as_view(),
        name='user_activity_create'
    ),
    url(
        r'^participants/(?P<pk>\d+)/attend/$',
        views.UserActivityAttendView.as_view(),
        name='user_activity_attend'
    ),
    url(
        r'^(?P<pk>\d+)/leave/$',
        views.UserActivityDeleteView.as_view(),
        name='user_activity_delete'
    ),
]

events_patterns = [
    url(
        r'^$',
        views.ActivityCreateView.as_view(),
        name='activity_create',
    ),
]
