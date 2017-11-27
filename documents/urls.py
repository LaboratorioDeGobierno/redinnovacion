from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^files/create/$',
        views.FileCreateView.as_view(),
        name='file_create',
    ),
    url(
        r'^files/(?P<pk>\d+)/delete/$',
        views.FileDeleteView.as_view(),
        name='file_delete',
    ),
    url(
        r'^photos/create/$',
        views.PhotoCreateView.as_view(),
        name='photo_create',
    ),
    url(
        r'^photos/(?P<pk>\d+)/delete/$',
        views.PhotoDeleteView.as_view(),
        name='photo_delete',
    ),
]
