from django.shortcuts import render, redirect
from user.models import SwSearchMasterTbl,HazCustomerMasterTbl
from django.views.generic import CreateView, UpdateView, DetailView, ListView, View
from django.utils.dateparse import parse_date
from datetime import date
from django.contrib import messages
from user.models import *
from bootstrap_modal_forms.generic import (
  BSModalCreateView,
  BSModalUpdateView,
  BSModalReadView,
  BSModalDeleteView
)
from .forms import *
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core import mail
from django.contrib.auth.mixins import LoginRequiredMixin
import base64
import requests
from django.contrib.auth.decorators import login_required


class DiscountCreateView(BSModalCreateView):
	template_name = 'products/create_discount.html'
	form_class = DiscountCreateForm
	success_url 	= '../../products/discount'

	def get_context_data(self, *args, **kwargs):
		context = super(DiscountCreateView, self).get_context_data(*args, **kwargs)
		context['title'] = "Product Price Update"
		return context

class UpdateDiscountView(BSModalCreateView):
	model = SwProductPricing
	template_name = 'products/update_discount.html'
	success_url 	= '../../pricing'
	form_class = DiscountCreateForm

	def post(self,*args,**kwargs):
		compname=self.request.POST['compName']
		companies=Company.objects.filter(compname=compname)
		company=Company.objects.get(compname=compname)
		Dis=DiscountTbl.objects.get(id=kwargs["id"])
		companies.update(discount=Dis)
		messages.success(self.request,"Added "+company.compname+" to Discount "+str(Dis.discount)+"%")
		return redirect('/products/discount')

	def get_context_data(self, *args, **kwargs):
		context = super(UpdateDiscountView, self).get_context_data(*args, **kwargs)
		company=Company.objects.all()
		context['title'] = "Product Discount Update"
		context['company']=company
		return context

class RemoveCompanyDiscountView(BSModalCreateView):
	model = SwProductPricing
	template_name = 'products/update_discount.html'
	success_url 	= '../../pricing'
	form_class = DiscountCreateForm

	def post(self,*args,**kwargs):
		compname=self.request.POST['compName']
		Dis=DiscountTbl.objects.get(id=kwargs["id"])
		companies=Company.objects.get(compname=compname)
		companies.discount=None
		companies.iquoteenabled=None
		companies.save()
		messages.error(self.request,"Removed "+companies.compname+" from Discount "+str(Dis.discount)+"%")
		return redirect('/products/discount')

	def get_context_data(self, *args, **kwargs):
		context = super(RemoveCompanyDiscountView, self).get_context_data(*args, **kwargs)
		Dis=DiscountTbl.objects.get(id=self.kwargs["id"]).id
		company=Company.objects.filter(discount=Dis)
		context['title'] = "Company Remove"
		context['company']=company
		return context

# Update Product Price
class UpdateProductView(BSModalUpdateView):
	model = SwProductPricing
	template_name = 'products/update_price.html'
	form_class = PriceUpdateForm
	success_url 	= '../../pricing'

	def get_context_data(self, *args, **kwargs):
		context = super(UpdateProductView, self).get_context_data(*args, **kwargs)
		context['title'] = "Product Price Update"
		return context

class PriceView(LoginRequiredMixin, ListView):
	template_name = "products/product_price.html"
	login_url = "/login/"
	model=SwProductPricing
	login_url = "/users/login"
	def get_context_data(self, *args, **kwargs):
		context = super(PriceView, self).get_context_data(**kwargs)
		products=SwProductPricing.objects.all()
		for a in products:
			total = a.product_price+a.sw_product_fees
			if a.product_gst_fees == "Yes" and a.sw_product_gst_fees == "Yes":
				messages.error(self.request,"Cannot check both GST on Services Fees and GST on Total")
			if a.product_gst_fees == "Yes":
				a.sw_product_gst_fees = "No"
				a.save()
				total+=a.product_price/10
			elif a.sw_product_gst_fees == "Yes":
				a.product_gst_fees = "No"
				a.save()
				total+=total/10

			a.total = total
			a.save()
		context['products'] = products
		return context


def products(request):
	return render(request,'products/order.html')


def email(request,*args,**kwargs):
	email=kwargs['email']
	message=EmailMessage(subject="THIS IS AN EMAIL", body="EMAAAAAAAAAAAAAAAAAAAAAAAAAIIIIIIIIIIIIIILLLLLLLLLLLLLLLLLLLLLLL",from_email=settings.DEFAULT_FROM_EMAIL,bcc=[email])
	attachment = open('haz_2_01d57c0e-6c36-11eb-8_SWR88G.pdf', 'rb')
	message.attach('haz_2_01d57c0e-6c36-11eb-8_SWR88G.pdf',attachment.read(),'application/pdf')
	message.send()
	messages.success(request,"Email sent to :"+str(email))
	return redirect('/products/transaction')

def discount(request):
	if request.user.is_superuser:
		discount=DiscountTbl.objects.all()
		company=Company.objects.all().exclude(discount=None)

		context={
		'discount':discount,
		'company':company
		}
		return render(request,'products/discount.html',context)
	else:
		return redirect("/users/login")

def transaction(request):
	if request.user.is_superuser:
		transaction = SwSearchMasterTbl.objects.all().exclude(internal_username ="External").order_by('-id')
		company=Company.objects.all()
		enrich_trans=[]
		for i in transaction:		

			try:
				comp=company.objects.get(companyid=i.customer_code)
			except:
				comp=None

			enrich_trans.append((i , comp))

		if request.POST:
			order 	= request.POST['order']
			start_date 	= request.POST['start_date']
			end_date 	= request.POST['end_date']
			client_ref = request.POST['client_ref']
			order_status= request.POST['order_status']
			
			# Allow search for product_status that is null
			if order_status=="NULL":
				trans=SwSearchMasterTbl.objects.filter(haz_order_id__icontains=order).filter(product_status__isnull=True).exclude(internal_username ="External").order_by('-id')
			else:
				trans=SwSearchMasterTbl.objects.filter(haz_order_id__icontains=order).filter(product_status__icontains=order_status).exclude(internal_username ="External").order_by('-id')
			enrich_trans=[]
			if client_ref:
				trans=trans.filter(applicantreferencenumber__icontains=client_ref).exclude(internal_username ="External").order_by('-id')
			if start_date:			
				trans=trans.filter(order_datetime__range=(parse_date(start_date),parse_date(end_date))).exclude(internal_username ="External").order_by('-id')

			for i in trans:
				try:
					comp=company.objects.get(companyid=i.customer_code)
				except:
					comp=None
					
				enrich_trans.append((i ,comp))

			context={
				'trs':enrich_trans,
				'order':order,
				'start_date':start_date,
				'end_date':end_date,
				'client_ref':client_ref,
				'order_status':order_status,
			}
			return render(request,'products/transaction.html',context)

		context={
			'trs':enrich_trans,
		}
		return render(request,'products/transaction.html',context)
	else:
		return redirect('/users/login')
		
@login_required
def getDocument(request):
	url = request.GET.get('pdf_slug', None)
	datapdf = ''
	if url == None:
		order_id = request.GET.get('order_id', None)
		prod = request.GET.get('product', None)
		order_id = order_id.replace("HAZPEXA", '')
		headers = {
			'Authorization': settings.AUTH_TOKEN,
			'FROM_ADMIN': 'Yes'
			}
		
		products = {'section66': 'SWR66C' , 'sewerServiceDiagram':'SWRSSD' , 'serviceLocationPrint':'SWRSLP' ,'buildingOverOrAdjacentToSewer': 'SWRBOA', 'specialMeterReading': 'SWRSMR' , 'section88G' : 'SWR88G'}
		
		datapdf = requests.get(url=f"{settings.API_URL}/sydwater/doc/pexa/haz_1_{order_id}_{products[prod]}.pdf", stream=True,headers=headers)
	else:
		
		url = url.replace(" ","%20")
		url = url.replace("https://api.hazlett.com.au", settings.API_URL)
		datapdf = requests.get(url=url, stream=True)

	response = render(request, 'products/document_broker.html')
	encoded = base64.b64encode(datapdf.content).decode('ascii')
	context = {"pdf_slug":encoded}
	
	if(datapdf.headers['Content-Type'] == 'application/pdf'):
		context = {"pdf_slug":"data:application/pdf;base64,"+encoded}
		context['pdf'] = True
		response = render(request, 'products/document_broker.html', context)
	else:
		context['data'] = datapdf.text
		context['pdf'] = False
		response = render(request, 'products/document_broker.html', context)

	return response

def getInvoiceStatus(request):
	invoice_id = request.GET.get('id', None)
	invoice_id = SwInvoice.objects.get(id=invoice_id)
	count  = InvoicePayment.objects.filter(invoice=invoice_id.id).count()

	if count > 0:
		return JsonResponse({"data": count, "items": list(InvoicePayment.objects.filter(invoice=invoice_id).values())})
	return JsonResponse({"data": count})

def getInvoiceStatusExternal(request):
	invoice_id = request.GET.get('id', None)
	invoice_id = SwInvoiceExternal.objects.get(id=invoice_id)
	count  = InvoicePaymentExternal.objects.filter(invoice=invoice_id.id).count()

	if count > 0:
		return JsonResponse({"data": count, "items": list(InvoicePaymentExternal.objects.filter(invoice=invoice_id).values())})
	return JsonResponse({"data": count})

def unpaidInvoice(request):
	invoice_id = request.POST.get("id", None)

	if invoice_id == None:
		return JsonResponse({"message": "Empty Fields", "status": False})

	try:
		invoice_id = SwInvoice.objects.get(id=invoice_id)

	except:
		return JsonResponse({"message": "Something went wrong", "status": False})

	invoice_id.payment_status = 'Unpaid'
	invoice_id.save()

	try:
		payment_instance = InvoicePayment.objects.get(invoice=invoice_id)
	except:
		return JsonResponse({"message": "Something went wrong", "status": False})

	payment_instance.delete()

	return JsonResponse({"message": "Payment Recorded", "status": True, "invoice_id": invoice_id.id})


def unpaidInvoiceExternal(request):
	invoice_id = request.POST.get("id", None)

	if invoice_id == None:
		return JsonResponse({"message": "Empty Fields", "status": False})

	try:
		invoice_id = SwInvoiceExternal.objects.get(id=invoice_id)

	except:
		return JsonResponse({"message": "Something went wrong", "status": False})

	invoice_id.payment_status = 'Unpaid'
	invoice_id.save()

	try:
		payment_instance = InvoicePaymentExternal.objects.get(invoice=invoice_id)
	except:
		return JsonResponse({"message": "Something went wrong", "status": False})

	payment_instance.delete()

	return JsonResponse({"message": "Payment Recorded", "status": True, "invoice_id": invoice_id.id})

def setInvoicePaid(request):
	invoice_id = request.POST.get('id', None)
	paymentMethod = request.POST.get('paymentMethod', None)
	date = request.POST.get('date', None)
	
	if invoice_id == None or paymentMethod == None:
		return JsonResponse({"message": "Empty Fields", "status": False})
	
	try:
		invoice_id = SwInvoice.objects.get(id=invoice_id)
	except:
		return JsonResponse({"message": "Something went wrong", "status": False})


	payment_instance = InvoicePayment.objects.create(
		is_paid = True,
		payment_method = paymentMethod,
		invoice = invoice_id
	)

	invoice_id.payment_status = 'Paid'
	invoice_id.save()
	payment_instance.save()

	return JsonResponse({"message": "Payment Recorded", "status": True, "invoice_id": invoice_id.id})


def setInvoicePaidExternal(request):
	invoice_id = request.POST.get('id', None)
	paymentMethod = request.POST.get('paymentMethod', None)
	date = request.POST.get('date', None)

	if invoice_id == None or paymentMethod == None:
		return JsonResponse({"message": "Empty Fields", "status": False})

	try:
		invoice_id = SwInvoiceExternal.objects.get(id=invoice_id)
	except:
		return JsonResponse({"message": "Something went wrong", "status": False})

	payment_instance = InvoicePaymentExternal.objects.create(
		is_paid=True,
		payment_method=paymentMethod,
		invoice=invoice_id
	)

	invoice_id.payment_status = 'Paid'
	invoice_id.save()
	payment_instance.save()

	return JsonResponse({"message": "Payment Recorded", "status": True, "invoice_id": invoice_id.id})


def externalDiscount(request):
	if request.user.is_superuser:
		discount=ExternalDiscountTbl.objects.all()
		company=CompanyExternal.objects.all().exclude(discount=None)
		context={
		'discount':discount,
		'company':company
		}
		return render(request,'swexternal/external_discount.html',context)
	else:
		return redirect("/users/login")

class externalDiscountCreateView(BSModalCreateView):
	form_class = ExternalDiscountCreateForm
	template_name = 'swexternal/external_create_discount.html'
	success_url 	= '../../external/discount'

	def form_valid(self, form):
		f = form.save(commit=False)
		print(form.cleaned_data['product_code'])
		if form.cleaned_data['product_code'] == "1":
			print("true")
			f.is_total = True
			f.product_code = None

		f.save
		return super().form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(externalDiscountCreateView, self).get_context_data(*args, **kwargs)
		context['title'] = "Product Price Update"
		return context

class externalUpdateDiscountView(BSModalCreateView):
	template_name = 'swexternal/external_create_discount.html'
	form_class = externalDiscountEditForm

	def get_initial(self):
		initial = super().get_initial()
		external_discount = ExternalDiscountTbl.objects.get(id=self.kwargs['id'])
		initial['discount'] = external_discount.discount
		initial['product_code'] = external_discount.product_code
		if external_discount.is_percent:
			initial['is_percent'] = 1
		else:
			initial['is_percent'] = 0
		return initial


	def post(self,*args,**kwargs):
		discount=self.request.POST['discount']
		is_percent = self.request.POST['is_percent']
		discount_instance = ExternalDiscountTbl.objects.filter(id=kwargs["id"])
		discount_instance.update(discount=float(discount), is_percent = is_percent )
		print("discount",discount)
		if discount_instance[0].is_total:
			messages.success(self.request,
							 "Edited Total Invoice to Discount " + str(discount) +
							 discount_instance[0].getSign())
		else:
			messages.success(self.request,"Edited "+discount_instance[0].product_code+" to Discount "+str(discount)+discount_instance[0].getSign())
		return redirect('/products/external/discount')

	def get_context_data(self, *args, **kwargs):
		context = super(externalUpdateDiscountView, self).get_context_data(*args, **kwargs)
		return context


def externalRemoveDiscount(request):
	in_id = request.POST.get('id', None)
	invoice = ExternalDiscountTbl.objects.get(id=in_id)
	invoice.delete()
	return JsonResponse({"success": True})


def externalTransaction(request):
	if request.user.is_superuser:
		transaction = SwSearchMasterTbl.objects.filter(internal_username = "External").order_by('-id')
		company = Company.objects.all()
		enrich_trans = []
		for i in transaction:

			try:
				comp = company.objects.get(companyid=i.customer_code)
			except:
				comp = None

			enrich_trans.append((i, comp))

		if request.POST:
			order = request.POST['order']
			start_date = request.POST['start_date']
			end_date = request.POST['end_date']
			client_ref = request.POST['client_ref']
			order_status = request.POST['order_status']

			# Allow search for product_status that is null
			if order_status == "NULL":
				trans = SwSearchMasterTbl.objects.filter(haz_order_id__icontains=order,internal_username = "External").filter(
					product_status__isnull=True).order_by('-id')
			else:
				trans = SwSearchMasterTbl.objects.filter(haz_order_id__icontains=order,internal_username = "External").filter(
					product_status__icontains=order_status).order_by('-id')
			enrich_trans = []
			if client_ref:
				trans = trans.filter(applicantreferencenumber__icontains=client_ref,internal_username = "External").order_by('-id')
			if start_date:
				trans = trans.filter(order_datetime__range=(parse_date(start_date), parse_date(end_date)),internal_username = "External").order_by(
					'-id')

			for i in trans:
				try:
					comp = company.objects.get(companyid=i.customer_code)
				except:
					comp = None

				enrich_trans.append((i, comp))

			context = {
				'trs': enrich_trans,
				'order': order,
				'start_date': start_date,
				'end_date': end_date,
				'client_ref': client_ref,
				'order_status': order_status,
			}
			return render(request, 'swexternal/external_transaction.html', context)

		context = {
			'trs': enrich_trans,
		}
		return render(request, 'swexternal/external_transaction.html', context)
	else:
		return redirect('/users/login')


class PriceExternalView(LoginRequiredMixin, ListView):
	template_name = "products/product_price_external.html"
	login_url = "/login/"
	model=SwProductPricingExternal
	login_url = "/users/login"
	def get_context_data(self, *args, **kwargs):
		context = super(PriceExternalView, self).get_context_data(**kwargs)
		products=SwProductPricingExternal.objects.all()
		for a in products:
			total = a.product_price+a.sw_product_fees
			if a.product_gst_fees == "Yes" and a.sw_product_gst_fees == "Yes":
				messages.error(self.request,"Cannot check both GST on Services Fees and GST on Total")
			if a.product_gst_fees == "Yes":
				a.sw_product_gst_fees = "No"
				a.save()
				total+=a.product_price/10
			elif a.sw_product_gst_fees == "Yes":
				a.product_gst_fees = "No"
				a.save()
				total+=total/10

			a.total = total
			a.save()
		context['products'] = products
		return context

class UpdateProductExternalView(BSModalUpdateView):
	print("PEXA")
	model = SwProductPricingExternal
	template_name = 'products/update_price.html'
	form_class = PriceUpdateForm
	success_url 	= '../../pricing'

	def get_context_data(self, *args, **kwargs):
		print("PEXA")
		context = super(UpdateProductExternalView, self).get_context_data(*args, **kwargs)
		context['title'] = "Pexa Product Price Update"
		return context