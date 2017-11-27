# -*- coding: utf-8 -*-
""" Decorators for the campaigns view """

# base
from base.serializers import ModelEncoder

# django
from django.http import HttpResponse

# standard library
import json


def json_view(view):
    def wrap(req, *args, **kwargs):
        response = view(req, *args, **kwargs)

        if isinstance(response, HttpResponse):
            http_response = response

        else:
            if isinstance(response, basestring):
                json_response = response
            else:
                json_response = json.dumps(response, cls=ModelEncoder)

            http_response = HttpResponse(json_response)

        http_response['Content-Length'] = len(http_response.content)
        http_response['Content-Type'] = "application/json"

        return http_response

    return wrap
