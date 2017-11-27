""" this document defines the project urls """

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('users.urls')),
    url(r'^institutions/', include('institutions.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^activities/', include('activities.urls')),
    url(r'^comments/', include('comments.urls')),
    url(r'^comments/', include('documents.urls')),
    url(r'^config/', include('configs.urls')),
    url(r'^notifications/', include('notifications.urls')),
    url(r'^documentation/', include('documentation.urls')),
    url(r'^dynamic-content/', include('dynamic_contents.urls')),
    url(r'^cases/', include('cases.urls')),
    url(r'^messages/', include('messaging.urls')),
    url(r'^newsletters/', include('newsletters.urls')),
    url(r'^admin/', include('loginas.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^api/v1/', include('api.urls')),
    url(r'^c/(?P<comment_id>\d+)/$', 'base.views.index', name='home'),
    url(r'^$', 'base.views.index', name='home'),
    url(r'^', include('evaluations.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    (r'^robots\.txt$', include('robots.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

# custom error pages
handler404 = 'base.views.page_not_found_view'
handler500 = 'base.views.error_view'
handler403 = 'base.views.permission_denied_view'
handler400 = 'base.views.bad_request_view'
