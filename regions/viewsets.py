from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import CountySerializer, RegionSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from .models import County, Region


class RegionViewset(viewsets.ReadOnlyModelViewSet):
    model = Region
    serializer_class = RegionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Region.objects.all()


class CountyViewset(viewsets.ReadOnlyModelViewSet):
    model = County
    serializer_class = CountySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('region',)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        name = self.request.GET.get('name', None)
        queryset = County.objects.all()
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
