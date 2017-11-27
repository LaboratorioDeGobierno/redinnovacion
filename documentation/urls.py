from django.conf.urls import include
from django.conf.urls import url

from . import views


methodology_urls = [
    url(
        r'^$',
        views.MethodologyListView.as_view(),
        name='methodology_list',
    ),
    url(
        r'^(?P<pk>[\d]+)/$',
        views.MethodologyDetailView.as_view(),
        name='methodology_detail'
    ),
    url(
        r'^create/$',
        views.MethodologyCreateView.as_view(),
        name='methodology_create'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.MethodologyUpdateView.as_view(),
        name='methodology_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.MethodologyDeleteView.as_view(),
        name='methodology_delete',
    ),
    url(
        r'^(?P<pk>[\d]+)/share/$',
        views.MethodologyShareView.as_view(),
        name='methodology_share',
    ),
]

tool_urls = [
    url(
        r'^$',
        views.ToolListView.as_view(),
        name='tool_list',
    ),
    url(
        r'^(?P<pk>[\d]+)/$',
        views.ToolDetailView.as_view(),
        name='tool_detail'
    ),
    url(
        r'^create/$',
        views.ToolCreateView.as_view(),
        name='tool_create'
    ),
    url(
        r'^create/methodology/(?P<methodology_pk>[\d]+)/$',
        views.ToolCreateView.as_view(),
        name='methodology_tool_create'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.ToolUpdateView.as_view(),
        name='tool_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.ToolDeleteView.as_view(),
        name='tool_delete',
    ),
    url(
        r'^(?P<pk>[\d]+)/share/$',
        views.ToolShareView.as_view(),
        name='tool_share',
    ),
]

publication_urls = [
    url(
        r'^$',
        views.PublicationListView.as_view(),
        name='publication_list',
    ),
    url(
        r'^(?P<pk>[\d]+)/$',
        views.PublicationDetailView.as_view(),
        name='publication_detail'
    ),
    url(
        r'^create/$',
        views.PublicationCreateView.as_view(),
        name='publication_create'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.PublicationUpdateView.as_view(),
        name='publication_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.PublicationDeleteView.as_view(),
        name='publication_delete',
    ),
    url(
        r'^(?P<pk>[\d]+)/share/$',
        views.PublicationShareView.as_view(),
        name='publication_share',
    ),
]

urlpatterns = [
    url(
        r'^$',
        views.MethodologyListView.as_view(),
        name='documentation_list',
    ),
    url(
        r'^file/(?P<hash_id>[0-9A-Fa-f-]+)/download/$',
        views.DownloadDocumentationFileView.as_view(),
        name='documentation_file_download',
    ),
    url(
        r'^search/$',
        views.DocumentationSearchView.as_view(),
        name='documentation_search',
    ),
    url(r'^methodology/', include(methodology_urls)),
    url(r'^tool/', include(tool_urls)),
    url(r'^publication/', include(publication_urls)),
]
