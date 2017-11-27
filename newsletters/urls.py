from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.NewsletterListView.as_view(),
        name='newsletter_list'
    ),
    url(
        r'^scenario/$',
        views.NewsletterScenarioView.as_view(),
        name='newsletter_scenario'
    ),
    url(
        r'^create/$',
        views.NewsletterCreateView.as_view(),
        name='newsletter_create'
    ),
    url(
        r'^(?P<pk>[\d]+)/$',
        views.NewsletterDetailView.as_view(),
        name='newsletter_detail'
    ),
    url(
        r'^(?P<pk>[\d]+)/email/$',
        views.NewsletterSendEmailView.as_view(),
        name='newsletter_send_email'
    ),
    url(
        r'^(?P<pk>[\d]+)/update/$',
        views.NewsletterUpdateView.as_view(),
        name='newsletter_update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete/$',
        views.NewsletterDeleteView.as_view(),
        name='newsletter_delete',
    ),
]
