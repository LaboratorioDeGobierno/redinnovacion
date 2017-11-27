# -*- coding: utf-8 -*-
from collections import OrderedDict

from django.db.models import Q

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from .serializers import UserSerializer
from .serializers import UserMentionSerializer
from .models import User


class UserLimitOffsetPagination(LimitOffsetPagination):
    page_size = 1

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('users', data)
        ]))


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    u'''
    Lista todos los usuarios del sistema con paginación.

    * `nombre de la url`: users-list

    * `q`: Buscador por nombre, apellido, cargo

        Ejemplo:

        ```
        curl -H "Authorization: Token 92c385e8844ecce7a5c806307a08a76ca8bb6cbb"
         -X GET "{url}/api/v1/users/?q={nombre}&format=json"
        ```

    * `limit`: Muestra X usuarios dependiendo del limite ?limit=2

    * `status`: Filtra por el código ingresado, las posibilidades son:

        * **0**: Pendiente
        * **1**: Aceptado
        * **2**: Rechazado

        Ejemplo:

        ```
        curl -H "Authorization: Token 92c385e8844ecce7a5c806307a08a76ca8bb6cbb"
         -X GET "{url}/api/v1/users/?status=1&format=json"
        ```


    * `institution`: Filtra por el pk de la institution:

        Ejemplo:

        ```
        curl -H "Authorization: Token 92c385e8844ecce7a5c806307a08a76ca8bb6cbb"
         -X GET "{url}/api/v1/users/?institution=1&format=json"
        ```


    * `is_staff`: Filtra si es administrador del sistema, las posibilidades
        son:

        * **True**: Es administrador
        * **False**: No es administrador

        Ejemplo:

        ```
        curl -H "Authorization: Token 92c385e8844ecce7a5c806307a08a76ca8bb6cbb"
        -X GET "{url}/api/v1/users/?is_staff=True&format=json"
        ```


    * `is_active`: Filtra si es esta activo o no (permisos de logeo en django),
    las posibilidades son:

        * **True**: Usuario activo
        * **False**: Usuario no esta activo en el sistema

        Ejemplo:

        ```
        curl -H "Authorization: Token 92c385e8844ecce7a5c806307a08a76ca8bb6cbb"
         -X GET "{url}/api/v1/users/?is_active=True&format=json"
        ```


    * Todos los filtros son concatenables:

        Ejemplo:

        ```
        curl -H "Authorization: Token 92c385e8844ecce7a5c806307a08a76ca8bb6cbb"
         -X GET "{url}/api/v1/users/?status=1&institution=1
         &is_active=True&is_staff=True&format=json"
        ```

    '''
    model = User
    serializer_class = UserSerializer
    pagination_class = UserLimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'status', 'institution', 'is_staff', 'is_active',)

    def get_serializer_class(self, *args, **kwargs):
        """
        Overridden to provide different serialization in the
        endpoint 'api/v1/users/mentionables/'
        """
        if self.action == 'mentionables':
            return UserMentionSerializer
        return self.serializer_class

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = User.objects.select_related('institution', 'region')
        if query:
            if self.request.GET.get('search_only_by_name'):
                for term in query.split(' '):
                    queryset = queryset.filter(
                        Q(first_name__icontains=term) |
                        Q(last_name__icontains=term)
                    )
            else:
                queryset = queryset.filter(
                    Q(first_name__icontains=query) |
                    Q(last_name__icontains=query) |
                    Q(mother_family_name__icontains=query) |
                    Q(charge__icontains=query) |
                    Q(institution__name__icontains=query) |
                    Q(region__name__icontains=query) |
                    Q(region__short_name__icontains=query)
                )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'users': serializer.data})

    @list_route()
    def mentionables(self, request, *args, **kwargs):
        """
        Returns all active users with a lightweight serialization
        """
        queryset = User.objects.filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'users': serializer.data})
