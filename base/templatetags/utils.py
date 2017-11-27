# -*- coding: utf-8 -*-
"""
Utils template tags
"""

# django
from django import template

register = template.Library()


@register.filter
def group(array, group_length):
    return zip(*(iter(array),) * group_length)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(is_safe=True)
def url_target_blank(text):
    return text.replace('<a ', '<a target="_blank" ')


@register.simple_tag(takes_context=True)
def query_parameters(context, order=None, type=None, language=None):
    """
    Returns a querystring to be used on links. For example pagination links

    type: set the type key on the querystring
    """
    # query string
    q = context.get('clean_query_string')

    # obtain all keys and values in the query string
    q_dict = {x[0]: x[1] for x in [x.split("=") for x in q.split("&") if x]}

    # replace type key if set
    if type:
        q_dict['type'] = type

    # replace type key if set
    if language is not None:
        q_dict['language'] = language

    q = '&'.join([u"{}={}".format(k, v) for k, v in q_dict.items()])

    # order
    if order is None:
        order = context.get('o_')

    if not (q or order):
        return u""

    # format url string
    order = u"o_={}".format(order) if order else ""
    _and = u"&" if q and order else ""

    return u"?{}{}{}".format(q, _and, order)
