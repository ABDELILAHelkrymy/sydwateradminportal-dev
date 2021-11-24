from django import template
from datetime import datetime
import pytz
register = template.Library()

def utc_to_sydney(d1):
    if d1 == None:
        return None
    try:
        d1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
    except TypeError:
        pass
    d2 = d1.replace(tzinfo=pytz.UTC)
    d3 = d2.astimezone(pytz.timezone("Australia/Sydney"))
    return d3.strftime('%Y-%m-%d %I:%M %p')
register.filter('to_sydney', utc_to_sydney)

def utc_to_manila(d1):
    d1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
    d2 = d1.replace(tzinfo=pytz.UTC)
    d3 = d2.astimezone(pytz.timezone("Asia/Manila"))
    return d3.strftime('%Y-%m-%d %H:%M:%S')
register.filter('to_manila', utc_to_manila)