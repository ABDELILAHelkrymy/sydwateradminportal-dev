from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import *
app_name = "product"

urlpatterns = [
	path('order/',login_required(products),name="order"),
	path('pricing/',PriceView.as_view(),name="price"),	
	path('email/<str:email>',login_required(email),name='email'),
	path('transaction/',transaction,name="transaction"),
	path('discount/',discount,name="discount"),
	path('update-product/<str:pk>/',login_required(UpdateProductView.as_view()),name='update_price'),
	path('update-discount/<int:id>/',login_required(UpdateDiscountView.as_view()),name='dis_add_company'),
	path('update-discount-remove/<int:id>/',login_required(RemoveCompanyDiscountView.as_view()),name='dis_remove_company'),
	path('create-discount/',login_required(DiscountCreateView.as_view()),name='create_discount'),
	path('pdf/view/', getDocument, name = 'view_pdf'),
	path('invoice/payment/', login_required(setInvoicePaid), name = 'invoice_paid'),
	path('invoice/payment/status/', login_required(getInvoiceStatus), name = 'invoice_status'),
	path('invoice/payment/unpaid/', login_required(unpaidInvoice), name = 'unpaidInvoice'),

	path('external/invoice/payment/', login_required(setInvoicePaidExternal), name='external_invoice_paid'),
	path('external/invoice/payment/status/', login_required(getInvoiceStatusExternal), name='external_invoice_status'),
	path('external/invoice/payment/unpaid/', login_required(unpaidInvoiceExternal), name='external_unpaidInvoice'),
	path('external/discount/', externalDiscount, name="external_discount"),
	path('external/create-discount/', login_required(externalDiscountCreateView.as_view()), name='external_create_discount'),
	path('external/update-discount/<int:id>/',login_required(externalUpdateDiscountView.as_view()),name='external_edit_discount'),
	path('external/update-discount-remove/', login_required(externalRemoveDiscount), name="external_remove_discount"),
	path('external/transaction/',externalTransaction,name="external_transaction"),

	path('external/pricing/',PriceExternalView.as_view(),name="external_price"),
	path('external/update-product/<str:pk>/',login_required(UpdateProductExternalView.as_view()),name='update_price_external'),

]