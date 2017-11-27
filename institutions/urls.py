from django.conf.urls import url

from . import views
from users.views import InstitutionUserCreateView

urlpatterns = [
    url(
        r'^$',
        views.InstitutionMostActiveListView.as_view(),
        name='institution_list'
    ),
    url(
        r'^most-active/$',
        views.InstitutionMostActiveListView.as_view(),
        name='institutions_list'
    ),
    url(
        r'^create/$',
        views.InstitutionCreateView.as_view(),
        name='institution_create'
    ),
    url(
        r'^(?P<slug>[\w-]+)/$',
        views.InstitutionDetailView.as_view(),
        name='institution_detail'
    ),
    url(
        r'^(?P<slug>[\w-]+)/add-user/$',
        InstitutionUserCreateView.as_view(),
        name='institution_user_create'
    ),
    url(
        r'^(?P<slug>[\w-]+)/update/$',
        views.InstitutionUpdateView.as_view(),
        name='institution_update'
    ),
    url(
        r'^(?P<slug>[\w-]+)/delete/$',
        views.InstitutionDeleteView.as_view(),
        name='institution_delete',
    ),
]
