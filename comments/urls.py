from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.CommentListView.as_view(),
        name='comment_list',
    ),
    url(
        r'^create/$',
        views.CommentCreateView.as_view(),
        name='comment_create',
    ),
    url(
        r'^create/answer/$',
        views.CommentAnswerCreateView.as_view(),
        name='comment_answer_create',
    ),
    url(
        r'^(?P<pk>\d+)/update/$',
        views.CommentUpdateView.as_view(),
        name='comment_update',
    ),
    url(
        r'^(?P<pk>\d+)/hide/$',
        views.CommentHideView.as_view(),
        name='comment_hide',
    ),
    url(
        r'^images/create/$',
        views.CommentImageCreateView.as_view(),
        name='comment_image_create',
    ),
    url(
        r'^likes/create/$',
        views.CommentLikeCreateView.as_view(),
        name='comment_like_create',
    ),
    url(
        r'^(?P<comment_id>\d+)/highlight/$',
        views.highlight_comment,
        name='comment_highlight_create',
    ),
]
