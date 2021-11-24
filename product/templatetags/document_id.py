from django import template
from django.conf import settings
register = template.Library()

def setDocID(id=1):
    return settings.INVOICE_URL +f'/file_download/?id={id}'

register.filter('setDocID', setDocID)

def setDocIDView(id=1):
    return settings.INVOICE_URL + f"/file_view/?id={id}"
register.filter('setDocIDView', setDocIDView)


def setDocIDExternal(id=1):
    return settings.INVOICE_URL +f'/external/file_download/?id={id}'

register.filter('setDocIDExternal', setDocIDExternal)

def setDocIDExternalView(id=1):
    return settings.INVOICE_URL + f"/external/file_view/?id={id}"
register.filter('setDocIDExternalView', setDocIDExternalView)

def setLRSDocID(id=1):
    return settings.LRS_INVOICING_URL +f'/file_download/?id={id}'

register.filter('setLRSDocID', setLRSDocID)

def setLRSDocIDView(id=1):
    return settings.LRS_INVOICING_URL + f"/file_view/?id={id}"
register.filter('setLRSDocIDView', setLRSDocIDView)

