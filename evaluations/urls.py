from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^activities/(?P<activity_id>\d+)/evaluate/$',
        views.EventEvaluationCreateView.as_view(),
        name='event_evaluation_create',
    ),
    url(
        r'^activities/(?P<activity_id>\d+)/evaluate/(?P<pk>\d+)/$',
        views.EventEvaluationUpdateView.as_view(),
        name='event_evaluation_update',
    ),
]
