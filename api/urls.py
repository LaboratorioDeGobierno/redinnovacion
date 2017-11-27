from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from api import views
from users.viewsets import UserViewSet
from regions.viewsets import CountyViewset, RegionViewset
from institutions.viewsets import InstitutionViewSet, InstitutionSimpleViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, 'users')
router.register(r'institutions', InstitutionViewSet, 'institutions')
router.register(
    r'institutions_simple', InstitutionSimpleViewSet, 'institutions_simple')
router.register(r'counties', CountyViewset, 'counties')
router.register(r'regions', RegionViewset, 'regions')

urlpatterns = [
    url(r'^oembed/$', views.get_oembed_data, name='get_oembed_data'),
    url(r'^', include(router.urls)),
]
