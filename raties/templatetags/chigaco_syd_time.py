"""Covert between America/Chicago and UTC time"""
from datetime import timedelta

from django import template

register = template.Library()


@register.filter(name='convert_chicago_to_sydney_time')
def convert_chicago_to_utc_time(value):
    """Convert Chicago to UTC time"""
    if value:
        return value + timedelta(hours=6)
    else:
        return value