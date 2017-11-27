from django.conf.urls import include
from django.conf.urls import url

from events import views
from activities.urls import events_patterns

stages_patterns = [


]

urlpatterns = [
    url(
        r'^$',
        views.EventListView.as_view(),
        name='event_list',
    ),
    url(
        r'^create/$',
        views.EventCreateView.as_view(),
        name='event_create',
    ),
    url(
        r'^(?P<pk>\d+)/update/$',
        views.EventUpdateView.as_view(),
        name='event_update',
    ),
    url(
        r'^(?P<pk>\d+)/delete/$',
        views.EventDeleteView.as_view(),
        name='delete_event',
    ),
    url(
        r'^(?P<pk>\d+)/$',
        views.EventDetailView.as_view(),
        name='event_detail',
    ),
    url(
        r'^(?P<pk>\d+)/c/(?P<comment_id>\d+)/',
        views.EventDetailView.as_view(),
        name='event_detail_with_comment',
    ),
    url(
        r'^calendar/$',
        views.events_calendar,
        name='calendar',
    ),
    url(
        r'^calendar/data/$',
        views.get_event_data,
        name='calendar_data',
    ),
    url(
        (
            r'^(?P<pk>\d+)/(?P<token>.+)&'
            r'(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$'
        ),
        views.event_detail_with_login,
        name='event_detail_with_login',
    ),
    url(
        r'^(?P<event_pk>\d+)/activities/',
        include(events_patterns),
    ),

    url(
        r'^(?P<event_pk>\d+)/stages/',
        views.StageCreateView.as_view(),
        name='stage_create',
    ),
    url(
        r'^stages/(?P<pk>\d+)/update/$',
        views.StageUpdateView.as_view(),
        name='stage_update_view',
    ),
    url(
        r'^stages/(?P<pk>\d+)/delete/$',
        views.StageDeleteView.as_view(),
        name='delete_stage',
    ),
    url(
        r'^stages/(?P<pk>\d+)/$',
        views.StageDetailView.as_view(),
        name='stage_detail',
    ),

    url(
        r'^attend/(?P<user_event_pk>\d+)/$',
        views.UserEventAttendView.as_view(),
        name='user_event_attend',
    ),
]
