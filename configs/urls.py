from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',
        views.AdminListView.as_view(),
        name='admin_list_view',
        ),
    url(r'^delete/admin/(?P<user_pk>\d+)/$',
        views.AdminDeleteRedirectView.as_view(),
        name='admin_delete_redirect_view',
        ),
]
