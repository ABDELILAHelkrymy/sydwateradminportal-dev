from django import template
from django.conf import settings
from lrs.models import *
register = template.Library()

def getPayload(id):
    data =""
    data = LrsPayload.objects.filter(referenceNumber= id).using('hazlrs_db')
    if len(data) < 1:
        data = None
    return data
register.filter('getPayload', getPayload)


def setRef(id):
    return settings.INVOICE_URL +f'/file_download/?id={id}'

register.filter('setRef', setRef)
