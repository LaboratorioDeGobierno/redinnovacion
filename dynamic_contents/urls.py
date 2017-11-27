from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^create/methodology/(?P<methodology_pk>[\d]+)/$',
        views.DynamicContentCreateView.as_view(),
        name='methodology_dynamic_content_create'
    ),
    url(
        r'^create/tool/(?P<tool_pk>[\d]+)/$',
        views.DynamicContentCreateView.as_view(),
        name='tool_dynamic_content_create'
    ),
    url(
        r'^create/case/(?P<case_pk>[\d]+)/$',
        views.DynamicContentCreateView.as_view(),
        name='case_dynamic_content_create'
    ),
    url(
        r'^(?P<pk>[\d]+)/$',
        views.DynamicContentDetailView.as_view(),
        name='dynamic_content_detail'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.DynamicContentUpdateView.as_view(),
        name='dynamic_content_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.DynamicContentDeleteView.as_view(),
        name='dynamic_content_delete',
    ),
]
