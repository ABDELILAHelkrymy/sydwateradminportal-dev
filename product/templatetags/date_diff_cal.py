from django import template
from datetime import datetime
register = template.Library()

def days_between(d1):
    d1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
    return abs((datetime.now() - d1).days)
register.filter('days_between', days_between)
