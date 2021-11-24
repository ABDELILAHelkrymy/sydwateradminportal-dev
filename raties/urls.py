from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import *
app_name = "raties"

urlpatterns = [
	path('document/detail/<int:pk>',ratiesDocumentDetails,name="raties_document_details"),
	path('document/',ratiesDocument,name="raties_document"),
	path('transaction', login_required(ratiesTransaction), name="raties_transaction"),
	path('transaction/details/<int:pk>',ratiesTransactionDetails,name="raties_transaction_details"),
	path('client/payload/details/<int:pk>',ratiesClientPayloadDetails.as_view(),name="raties_client_payload_details"),
	path('invoice/', login_required(ratiesInvoicing), name="raties_invoice"),
	path('invoice/payment/status/', login_required(getRatiesInvoiceStatus), name='raties_invoice_status'),
	path('invoice/payment/', login_required(setRatiesInvoicePaid), name='raties_invoice_paid'),
	path('invoice/payment/unpaid/', login_required(setRatiesUnpaidInvoice), name='raties_unpaidInvoice'),
	path('invoice/edit', login_required(ratiesManualCreation), name="raties_invoice_view_edit"),
	path('invoice/item/remove', login_required(ratiesRemoveInvoice), name="raties_invoice_item_remove"),
	path('invoice/add', login_required(ratiesAddInvoiceItem), name="raties_invoice_add"),

	path('invoice/file_download', login_required(getInvoiceFile), name="raties_invoice_download"),
	path('invoice/update', invoiceGenerate,  name="raties_invoice_update"),

	path('service', GroupServiceChargesView,  name="raties_service_charge"),
	path('service/create', login_required(GroupServiceChargesCreateView.as_view()), name='raties_service_charge_create'),
	path('service/test/update/<int:id>/', login_required(ratiesUpdateServiceCharge.as_view()), name='raties_service_charge_update'),
	path('service/remove', login_required(ratiesRemoveServiceCharge), name="raties_service_charge_remove"),



    path('authcouncil', AuthCouncil,  name="raties_auth_council"),
    path('authcouncil/create', login_required(AuthCouncilCreateView.as_view()),name='raties_auth_council_create'),
	path('authcouncil/update/<int:id>/', login_required(AuthCouncilUpdateView.as_view()), name='raties_auth_council_update'),
	path('authcouncil/remove', login_required(AuthCouncilRemove), name="raties_auth_council_remove"),

	path('authority', Authority,  name="raties_authority"),
	path('authority/create', login_required(AuthorityCreateView.as_view()),name='raties_authority_create'),
	path('authority/update/<int:id>/', login_required(AuthorityUpdateView.as_view()), name='raties_authority_update'),
	path('authority/remove', login_required(AuthorityRemove), name="raties_authority_remove"),


	path('reset', login_required(reset_raties_db), name="raties_reset"),


	#path('template', login_required(ratiesTemplate), name="raties_template"),
	path('form/<int:id>/', login_required(ratiesTemplate), name="raties_template"),
	path('form/download/<int:id>/', login_required(ratiesDownloadForm), name="raties_form_load"),

    path('document/file/upload/<int:pk>/<int:id>/', login_required(simple_upload), name='raties_document_file_upload'),
	path('transaction/file/upload/<int:pk>/', login_required(transaction_upload), name='raties_transaction_upload'),
	path('transaction/status/<int:pk>/', login_required(TransactionStatus), name='raties_status'),



	path('product', login_required(ProductView), name="raties_product"),
	path('product/create', login_required(ProductCreateView.as_view()),name='raties_product_create'),
	path('product/update/<int:id>/', login_required(ProductUpdateView.as_view()),name='raties_product_update'),
	path('product/remove', login_required(ProductRemoveView), name="raties_product_remove"),


]