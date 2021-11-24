from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import *
app_name = "lrs"

urlpatterns = [
	path('home/',lrsHome,name="lrs_home"),
	path('home/download/<file>', login_required(lrsDownloadFile), name="download"),
	path('invoice/',login_required(lrsInvoicing), name="lrs_invoice"),
	path('pricing/',login_required(lrsPricingView.as_view()), name="lrs_pricing"),
	path('update-product/<str:pk>/', login_required(UpdateLrsProductView.as_view()), name='lrs_update_price'),

	path('invoice/payment/status/', login_required(getLrsInvoiceStatus), name = 'lrs_invoice_status'),
	path('invoice/payment/', login_required(setLrsInvoicePaid), name='lrs_invoice_paid'),
	path('invoice/payment/unpaid/', login_required(setLrsUnpaidInvoice), name = 'lrs_unpaidInvoice'),

	path('invoice/edit',login_required(lrsManualCreation),name="lrs_invoice_view_edit"),

	path('invoice/item/remove', login_required(lrsRemoveInvoice), name="lrs_invoice_item_remove"),
	path('invoice/add',login_required(lrsAddInvoiceItem) ,name="lrs_invoice_add"),

	path('discount/', discount, name="lrs_discount"),
	path('create-discount/', login_required(DiscountCreateView.as_view()), name='lrs_create_discount'),
	path('update-discount/<int:id>/',login_required(UpdateDiscountView.as_view()),name='lrs_dis_add_company'),
	#path('update-discount-remove/<int:id>/', login_required(RemoveCompanyDiscountView.as_view()), name='lrs_dis_remove_company'),
	path('update-discount-remove/', login_required(lrsRemoveDiscount), name="lrs_dis_remove"),


	path('logs/',login_required(lrsLogsView.as_view()), name="logs"),
	path('logs/<file>',login_required(lrsLogsDetailsView), name="logs_view"),
	path('payments', login_required(payments), name="lrs_payments_view"),
	path('transaction/payload/', login_required(payloadView), name= "lrs_payloadView"),
	path('document/',lrsDocument,name="Document"),
	path('document/payload/',lrsDocumentView,name="document_view"),
]