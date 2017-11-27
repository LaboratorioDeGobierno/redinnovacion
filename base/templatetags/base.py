# -*- coding: utf-8 -*-
"""
Template tags common to all apps of this project
"""
from django import template

register = template.Library()


@register.filter(is_safe=True)
def url_target_blank(text):
    return text.replace('<a ', '<a target="_blank" ')
