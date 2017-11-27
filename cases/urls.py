from django.conf.urls import include
from django.conf.urls import url

from . import views


case_urls = [
    url(
        r'^$',
        views.CaseListView.as_view(),
        name='case_list',
    ),
    url(
        r'^(?P<pk>[\d]+)/$',
        views.CaseDetailView.as_view(),
        name='case_detail'
    ),
    url(
        r'^create/$',
        views.CaseCreateView.as_view(),
        name='case_create'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.CaseUpdateView.as_view(),
        name='case_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.CaseDeleteView.as_view(),
        name='case_delete',
    ),
    url(
        r'^(?P<pk>[\d]+)/share/$',
        views.CaseShareView.as_view(),
        name='case_share',
    ),
    url(
        r'^file/create/$',
        views.FileCreateView.as_view(),
        name='case_file_create',
    ),
    url(
        r'^search/$',
        views.CaseSearchView.as_view(),
        name='case_search'
    ),
]

urlpatterns = [
    url(r'^', include(case_urls)),
]
