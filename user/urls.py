from django.urls import path, include
from django.contrib.auth import views as authViews
from django.contrib.auth.decorators import login_required
from .views import *
app_name = "user"
#this is the urls
urlpatterns = [
	path('login/',AdminLoginView,name='login'),
	path('logout/',logoutView,name='logout'),
	path('add_user',UserCreate.as_view(),name="add_user"),
	path('invoice',login_required(invoicing),name="invoice_view"),
	path('add_company',CompanyCreate.as_view(),name="add_company"),
	path('invoice/edit',login_required(manualCreation),name="invoice_view_edit"),
	path('invoice/add',login_required(addInvoiceItem) ,name="invoice_add"),
	path('invoice/item/save',login_required(saveinvoicerow) ,name="invoice_item_save"),
	path('invoice/item/remove',login_required(removeInvoice) ,name="invoice_item_remove"),
	path('email/log',login_required(emailLog) ,name="mail_log"),
	path('email/reset',login_required(resetMailLog) ,name="reset_mail"),
	path('mail/all/logs', login_required(getlogsmail), name= "get_mails_logs"),
	path('application/check', login_required(getApplicationStatus), name= "application_check"),
	path('user/emails', login_required(viewEmail), name= "viewEmail"),
	path('user/email/update', login_required(updateMail), name= "updateMail"),
	path('document/resend', login_required(resetDocumentStatus), name= "resetDocumentStatus"),
	path('company/edit', login_required(companyEditView), name= "companyEditView"),
	path('company/edit/<int:pk>/', login_required(companyEditSave), name= "companyEditSave"),
	path('company/delete', login_required(companyDelete), name= "companyDelete"),
	path('transaction/payload/', login_required(payloadView), name= "payloadView"),
	path('payments',login_required(payments),name="payments_view"),
	path('appselector',login_required(appSelectorView),name="appselector_view"),


    path('external/invoice',login_required(invoicingExternal),name="external_invoice_view"),
	path('external/invoice/edit', login_required(manualCreationExternal), name="external_invoice_view_edit"),
	path('external/invoice/item/remove', login_required(removeInvoiceExternal), name="external_invoice_item_remove"),
	path('external/invoice/add', login_required(addInvoiceItemExternal), name="external_invoice_add"),
	path('external/invoice/item/save', login_required(saveinvoicerowExternal), name="external_invoice_item_save"),
	path('external/payments',login_required(external_payments),name="external_payments_view"),

]