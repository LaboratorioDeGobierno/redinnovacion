# -*- coding: utf-8 -*-
from collections import OrderedDict

from django.db.models import Q

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.settings import api_settings
from rest_framework.renderers import JSONRenderer

from .serializers import InstitutionSerializer, InstitutionSimpleSerializer
from .models import Institution


class InstitutionLimitOffsetPagination(LimitOffsetPagination):
    page_size = 1

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('institutions', data)
        ]))


class InstitutionSimpleViewSet(viewsets.ReadOnlyModelViewSet):
    model = Institution
    serializer_class = InstitutionSimpleSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = InstitutionLimitOffsetPagination
    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Institution.objects.active()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'institutions': serializer.data})


class InstitutionViewSet(InstitutionSimpleViewSet):
    u'''
        * `nombre de la url`: institutions-list

        * `q`: Buscador por nombre de la institución

        * `has_users`: Muestra solamente las instituciones que tengan usuarios
        ?has_users=true

        * `limit`: Muestra X instituciones dependiendo del limite ?limit=2
    '''
    serializer_class = InstitutionSerializer
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def get_queryset(self):
        queryset = super(InstitutionViewSet, self).get_queryset()
        query = self.request.GET.get('q', None)
        has_users = self.request.GET.get('has_users', None)
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
            )
        if has_users:
            queryset = queryset.has_users()
        return queryset
