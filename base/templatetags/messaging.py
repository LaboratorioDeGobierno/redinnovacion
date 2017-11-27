# -*- coding: utf-8 -*-

# django
from django import template
from django.utils import timezone

register = template.Library()


@register.filter(name='get_datetime_last_message')
def get_datetime_last_message(obj, user):
    """Get datetime from last message between 2 users"""
    last_message = obj.get_last_message(user)
    return last_message.created_at


@register.filter(name='is_today')
def is_today(obj):
    """Check if the datetime obj is today"""
    today = timezone.localtime(timezone.now()).date()
    return obj.date() == today
