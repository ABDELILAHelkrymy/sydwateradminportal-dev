from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DetailView, ListView, View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .views import *
from .forms import *
from django.contrib.auth.models import User
from .models import *
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import requests
import json
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q
def AdminLoginView(request):
	user=None
	if request.method=="GET":
		if request.user.is_superuser:
			return redirect('/products/transaction')
		else:
			return render(request,'users/login.html')

	if request.method == "POST":
		username_login=request.POST['username']
		password_login=request.POST['password']
		user=authenticate(request,username=username_login, password=password_login)
		if user is not None:
			login(request,user)
			if request.user.is_superuser:			
				return redirect('/users/appselector')
			else:
				logout(request)
				return redirect('/users/login')
	
	return render(request,'users/login.html')

class UserCreate(LoginRequiredMixin,CreateView):
	template_name = "users/addUser.html"
	login_url = "/users/login"
	form_class = AddUserForm

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		try:
			context['company']=Company.objects.all().order_by('compname')
		except:
			context['company']=None
		return context

	def post(self, request, *args, **kwargs):
		account 	= request.POST['userAccountName']
		username 	= request.POST['userUserName']
		password 	= request.POST['userPassword']
		re_password = request.POST['userRePassword']
		order_status= request.POST['orderStatus']
		compName 	= request.POST['compName']
		try:
			z=UserCustomer.objects.get(username=username)
			messages.error(request, 'User name already exist')
			return redirect('/users/add_user')
		except:
			if password == re_password:
				company = Company.objects.get(compname=compName)
				date=now()
				real_username=account+"+"+username
				hashed_password=make_password(password)
				Auth=AuthUser.objects.create(username=real_username,password=hashed_password, date_joined=now(),is_active=1,is_superuser=0,is_staff=1,first_name=username,last_name=account)
				Auth.save()
				asw=UserCustomer.objects.create(account=account, username=real_username, password=password, order_status=order_status,user=Auth, company=company)
			else:
				messages.error(request, 'password is not same')
				return redirect('/users/add_user')

		success="User "+username+" Added Succesfully"
		messages.success(request,str(success))
		return redirect('/users/add_user')


class CompanyCreate(LoginRequiredMixin,CreateView):
	template_name = "users/addCompany.html"
	login_url = "/users/login"
	form_class = AddUserForm
	redirect_field_name = '/users/add_company'

	def get_context_data(self, *args, **kwargs):
		return super().get_context_data(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		compId 	= request.POST['compId']
		compName 	= request.POST['compName']
		compCode = request.POST['compCode']
		compStreet= request.POST['compStreet']
		compSuburb 	= request.POST['compSuburb']
		compState 	= request.POST['compState']
		compPostcode 	= request.POST['compPostcode']
		compPhone = request.POST['compPhone']
		mailStreet= request.POST['mailStreet']
		mailSuburb 	= request.POST['mailSuburb']
		mailState 	= request.POST['mailState']
		mailPostcode 	= request.POST['mailPostcode']
		directContact = request.POST['directContact']
		directContactNumber= request.POST['directContactNumber']
		directContactMobile 	= request.POST['directContactMobile']
		directFaxNumber 	= request.POST['directFaxNumber']
		faxNumberAreaCode 	= request.POST['faxNumberAreaCode']
		compFax = request.POST['compFax']
		compEmail= request.POST['compEmail']
		compDirectPhoneNumberAreaCode 	= request.POST['compDirectPhoneNumberAreaCode']
		compHomePhoneNumberAreaCode 	= request.POST['compHomePhoneNumberAreaCode']
		clientonline 	= request.POST['clientonline']
		groupIdManual = request.POST['groupIdManual']
		CompanyACN= request.POST['CompanyACN']
		CompanyABN 	= request.POST['CompanyABN']
		try:
			Company.objects.get(companyindex=compIndex)
			messages.error(request, 'Company already exist')
			return redirect('/users/add_company')
		except:
			Company.objects.create(companyid=compId,compname=compName,compcode=compCode,compstreet=compStreet,compsuburb=compSuburb,compstate=compState,comppostcode=compPostcode,compphone1=compPhone,mailstreet=mailStreet,
				mailsuburb=mailSuburb,mailstate=mailState,mailpostcode=mailPostcode,directcontact=directContact,directcontactnumber=directContactNumber,directcontactmobile=directContactMobile,directfaxnumber=directFaxNumber,faxnumberareacode=faxNumberAreaCode,
				compfax1=compFax,compemail1=compEmail,compdirectphonenumberareacode=compDirectPhoneNumberAreaCode,comphomephonenumberareacode=compHomePhoneNumberAreaCode,clientonline=clientonline,groupidmanual=groupIdManual,companyacn=CompanyACN,companyabn=CompanyABN)
			
		success="Company "+compName+" Added Succesfully"
		messages.success(request,str(success))
		return redirect('/users/add_company')

def logoutView(request):
	logout(request)
	return redirect('/users/login')

def invoicing(request):
	if request.user.is_superuser:
		if request.method == 'GET':
			data = SwInvoice.objects.all().order_by('-id')
			return render(request, "invoicing/invoice.html", context={"data": data})
		else:
			fromdate = request.POST.get('from', None)
			todate = request.POST.get("to", None)

			if fromdate == None:
				data = SwInvoice.objects.filter(searches_to=todate).order_by('-id')
			if todate == None:
				data = SwInvoice.objects.filter(searches_from=fromdate).order_by('-id')
			
			if todate == None and fromdate == None:
				data = SwInvoice.objects.all().order_by('-id')
				
			if todate != None and fromdate != None:
				data = SwInvoice.objects.filter(searches_to=todate,searches_from=fromdate).order_by('-id')
				
			return render(request, "invoicing/invoice.html", context={"data": data})		
	else:
		return redirect("/users/login")


def invoicingExternal(request):
	if request.user.is_superuser:
		if request.method == 'GET':
			data = SwInvoiceExternal.objects.all().order_by('-id')
			return render(request, "invoicing/invoice_external.html", context={"data": data})
		else:
			fromdate = request.POST.get('from', None)
			todate = request.POST.get("to", None)

			if fromdate == None:
				data = SwInvoiceExternal.objects.filter(searches_to=todate).order_by('-id')
			if todate == None:
				data = SwInvoiceExternal.objects.filter(searches_from=fromdate).order_by('-id')

			if todate == None and fromdate == None:
				data = SwInvoiceExternal.objects.all().order_by('-id')

			if todate != None and fromdate != None:
				data = SwInvoiceExternal.objects.filter(searches_to=todate, searches_from=fromdate).order_by('-id')

			return render(request, "invoicing/invoice_external.html", context={"data": data})
	else:
		return redirect("/users/login")

# Define a method to filter payment records by date
def get_payments_by_date(fromdate, todate):
	if fromdate == None:
		payments_queryset = InvoicePayment.objects.select_related('invoice').filter(payment_date__range=(todate, todate))
	if todate == None:
		payments_queryset = InvoicePayment.objects.select_related('invoice').filter(payment_date__range=(fromdate, fromdate))	
	if todate == None and fromdate == None:
		payments_queryset = InvoicePayment.objects.select_related('invoice')	
	if todate != None and fromdate != None:
		payments_queryset = InvoicePayment.objects.select_related('invoice').filter(payment_date__range=(fromdate, todate))

	data_array=[]
	# List of required invoice ids
	invoiceid_list = payments_queryset.values_list('invoice', flat=True)
	invoice_queryset = SwInvoice.objects.filter(id__in=invoiceid_list)

	for payment in payments_queryset:
		invoice_data = invoice_queryset.filter(id=payment.invoice.id)

		new_amount = invoice_data[0].total_price - invoice_data[0].gst_charge

		new_data = {
			"payment_date": payment.payment_date.date(),
			"type": payment.payment_method,
			"amount": new_amount,
			"gst": invoice_data[0].gst_charge,
			"total": invoice_data[0].total_price,
			"place_holder": ""
		}

		data_array.append(new_data)

	return data_array

def get_external_payments_by_date(fromdate, todate):
	if fromdate == None:

		payments_queryset = InvoicePaymentExternal.objects.select_related('invoice').filter(payment_date__range=(todate, todate))
	if todate == None:
		payments_queryset = InvoicePaymentExternal.objects.select_related('invoice').filter(payment_date__range=(fromdate, fromdate))
	if todate == None and fromdate == None:
		payments_queryset = InvoicePaymentExternal.objects.select_related('invoice')
	if todate != None and fromdate != None:
		payments_queryset = InvoicePaymentExternal.objects.select_related('invoice').filter(payment_date__range=(fromdate, todate))

	data_array=[]
	# List of required invoice ids
	invoiceid_list = payments_queryset.values_list('invoice', flat=True)
	invoice_queryset = SwInvoiceExternal.objects.filter(id__in=invoiceid_list)

	for payment in payments_queryset:
		invoice_data = invoice_queryset.filter(id=payment.invoice.id)

		new_amount = invoice_data[0].total_price - invoice_data[0].gst_charge

		new_data = {
			"payment_date": payment.payment_date.date(),
			"type": payment.payment_method,
			"amount": new_amount,
			"gst": invoice_data[0].gst_charge,
			"total": invoice_data[0].total_price,
			"place_holder": ""
		}

		data_array.append(new_data)

	return data_array

def payments(request):
	if request.user.is_superuser:
		if request.method == 'GET':
			# Get all records
			payments = InvoicePayment.objects.select_related('invoice')
			# Dates range object
			date_range= {
				"from_date": payments.first().payment_date.date(),
				"to_date": payments.last().payment_date.date()
			}

			data=[]
			# List of required invoice ids
			invoiceid_list = payments.values_list('invoice', flat=True)
			invoice_queryset = SwInvoice.objects.filter(id__in=invoiceid_list)
			for payment in payments:
				invoice_data = invoice_queryset.filter(id=payment.invoice.id)

				new_amount = invoice_data[0].total_price - invoice_data[0].gst_charge

				new_data = {
				"payment_date": payment.payment_date.date(),
				"type": payment.payment_method,
				"amount": new_amount,
				"gst": invoice_data[0].gst_charge,
				"total": invoice_data[0].total_price,
				"place_holder": ""
				}

				data.append(new_data)

			return render(request, "invoicing/payments.html", context={"data": data, "date_range": date_range})
		else:
			fromdate = request.POST.get('from', None)
			todate = request.POST.get("to", None)
			# Create dates object
			date_range = {
				"from_date": fromdate,
				"to_date": todate
			}
			# Get required data using the dates
			data = get_payments_by_date(fromdate, todate)
							
			return render(request, "invoicing/payments.html", context={"data": data, "date_range": date_range})		
	else:
		return redirect("/users/login")

def manualCreation(request):
	if request.method == 'GET':

		company_code = request.GET.get('id')
		invoice_id = request.GET.get('in')
		data = InvoiceItems.objects.filter(invoice=invoice_id)
		transactions = SwSearchMasterTbl.objects.filter(internal_username__contains=company_code + '+')
		return render(request, "invoicing/invoice_create.html", context={ "data": data, "transactions": transactions, "invoice_id":invoice_id})

def manualCreationExternal(request):
	if request.method == 'GET':

		company_code = request.GET.get('id')
		invoice_id = request.GET.get('in')
		data = InvoiceItemsExternal.objects.filter(invoice=invoice_id)
		transactions = SwSearchMasterTbl.objects.filter(internal_username__contains=company_code + '+')
		return render(request, "invoicing/invoice_create_external.html", context={ "data": data, "transactions": transactions, "invoice_id":invoice_id})

		
def addInvoiceItem(request):
	username = request.POST.get("username", None)
	date_ordered = request.POST.get("date_ordered", None)
	reference = request.POST.get("reference", None)
	client_reference = request.POST.get("client", None)
	invoice_id = request.POST.get("invoice_id", None)

	invoice_instance = SwInvoice.objects.get(id=invoice_id)

	disb = request.POST.get("disb", 5.0)
	charge = request.POST.get("charge", 3.0)
	gst = request.POST.get("gst", 0.5)

	disb_charge = float(disb) + float(charge)

	gst_inc = float(gst) + disb_charge

	last_item = InvoiceItems.objects.filter(invoice=invoice_instance.id).order_by('count').last()

	instance = InvoiceItems.objects.create(
		count = last_item.count + 1,
		username = username,
		date_ordered = date_ordered,
		reference=reference,
		client_reference=client_reference,
		disb=disb,
		charge=charge,
		disb_charge=disb_charge,
		gst_amount=gst,
		gst_inc=gst_inc,
		include=1,
		transaction=None,
		invoice = invoice_instance
	)

	instance.save()
	
	return JsonResponse({
		"username": instance.username,
		"date_ordered": instance.date_ordered,
		"reference": "Sydney Water Search",
		"client_reference": instance.client_reference,
		"disb": str(disb),
		"charge": str(charge),
		"gst": str(gst),
		"total": str(disb_charge),
		"gst_total": str(gst_inc),
		"count": str(instance.count),
		"id": instance.id
	})


def addInvoiceItemExternal(request):
	username = request.POST.get("username", None)
	date_ordered = request.POST.get("date_ordered", None)
	reference = request.POST.get("reference", None)
	client_reference = request.POST.get("client", None)
	invoice_id = request.POST.get("invoice_id", None)

	invoice_instance = SwInvoiceExternal.objects.get(id=invoice_id)

	disb = request.POST.get("disb", 5.0)
	charge = request.POST.get("charge", 3.0)
	gst = request.POST.get("gst", 0.5)

	disb_charge = float(disb) + float(charge)

	gst_inc = float(gst) + disb_charge

	last_item = InvoiceItemsExternal.objects.filter(invoice=invoice_instance.id).order_by('count').last()

	instance = InvoiceItemsExternal.objects.create(
		count=last_item.count + 1,
		username=username,
		date_ordered=date_ordered,
		reference=reference,
		client_reference=client_reference,
		disb=disb,
		charge=charge,
		disb_charge=disb_charge,
		gst_amount=gst,
		gst_inc=gst_inc,
		include=1,
		transaction=None,
		invoice=invoice_instance
	)

	instance.save()

	return JsonResponse({
		"username": instance.username,
		"date_ordered": instance.date_ordered,
		"reference": "Sydney Water Search",
		"client_reference": instance.client_reference,
		"disb": str(disb),
		"charge": str(charge),
		"gst": str(gst),
		"total": str(disb_charge),
		"gst_total": str(gst_inc),
		"count": str(instance.count),
		"id": instance.id
	})

def removeInvoice(request):
	in_id = request.POST.get('id', None)
	invoice = InvoiceItems.objects.get(id=in_id)
	invoice.delete()
	return JsonResponse({"success": True})

def removeInvoiceExternal(request):
	in_id = request.POST.get('id', None)
	invoice = InvoiceItemsExternal.objects.get(id=in_id)
	invoice.delete()
	return JsonResponse({"success": True})
		
def getDataDetails(request):
	sw_id = request.POST.get('id', None)
	data = SwSearchMasterTbl.objects.get(id=sw_id)

	products = {
		'section66':'SWR66C', 
		'sewerServiceDiagram' : 'SWRSSD', 
		'serviceLocationPrint' : 'SWRSLP', 
		'buildingOverOrAdjacentToSewer' : 'SWRBOA', 
		'specialMeterReading' : 'SWRSMR', 
		'section88G' : 'SWR88G'
		}
	# print(data.)
	
	prod = SwProductsTbl.objects.get(product_code=products[data.product_name])
	prod_price = SwProductPricing.objects.get(product_code=products[data.product_name])
	last_item = InvoiceItems.objects.filter(invoice__cmpany_code=data.internal_username.split('+')[0]).last()
	
	gst = 0

	if prod_price.product_gst_fees == "Yes":
		gst = 0.1 *  prod_price.product_price
	else:
		gst = 0.1 *  prod_price.sw_product_fees
	
	context = {
		"data_id": data.id,
		"username": data.internal_username.split('+')[-1],
		"date_ordered": data.order_datetime.strftime('%B %d, %Y'),
		"reference": "Sydney Water Search",
		"client_reference": data.applicantreferencenumber,
		"disb": str(prod_price.sw_product_fees),
		"charge": str(prod_price.product_price),
		"gst": str(gst),
		"total": str(prod_price.sw_product_fees + prod_price.product_price),
		"gst_total": str(prod_price.sw_product_fees + prod_price.product_price + gst),
		"count": str(last_item.count + 1),
		"transac_id": sw_id
		}
	return JsonResponse({"data": context})

def saveinvoicerow(request):
	disb = request.POST.get("disb", None)
	charge = request.POST.get("charge", None)
	disb_charge = request.POST.get("total", None)
	gst_amount = request.POST.get("gst", None)
	gst_inc = request.POST.get("gst_total", None)
	sw_id = request.POST.get("transac_id", None)
	invoice = request.POST.get("invoice_id", None)

	invoice_instance = SwInvoice.objects.get(id=invoice)

	transac_instance = SwSearchMasterTbl.objects.get(id=sw_id)

	last_item = InvoiceItems.objects.filter(invoice__cmpany_code=transac_instance.internal_username.split('+')[0]).last()

	invoice_item_instance = InvoiceItems.objects.create(
		count = last_item.count + 1,
		username= transac_instance.internal_username.split('+')[-1],
		date_ordered= transac_instance.order_datetime,
		reference= "Sydney Water Search",
		client_reference= transac_instance.applicantreferencenumber,
		disb= disb,
		charge= charge,
		disb_charge= disb_charge,
		gst_amount= gst_amount,
		gst_inc= gst_inc,
		transaction= transac_instance.id,
		invoice= invoice_instance,
	)

	invoice_item_instance.save()

	return JsonResponse({"data": "invoice saved", "invoice_id": invoice_item_instance.id})

def saveinvoicerowExternal(request):
	disb = request.POST.get("disb", None)
	charge = request.POST.get("charge", None)
	disb_charge = request.POST.get("total", None)
	gst_amount = request.POST.get("gst", None)
	gst_inc = request.POST.get("gst_total", None)
	sw_id = request.POST.get("transac_id", None)
	invoice = request.POST.get("invoice_id", None)

	invoice_instance = SwInvoiceExternal.objects.get(id=invoice)

	transac_instance = SwSearchMasterTbl.objects.get(id=sw_id)

	last_item = InvoiceItemsExternal.objects.filter(invoice__cmpany_code=transac_instance.internal_username.split('+')[0]).last()

	invoice_item_instance = InvoiceItemsExternal.objects.create(
		count = last_item.count + 1,
		username= transac_instance.internal_username.split('+')[-1],
		date_ordered= transac_instance.order_datetime,
		reference= "Sydney Water Search",
		client_reference= transac_instance.applicantreferencenumber,
		disb= disb,
		charge= charge,
		disb_charge= disb_charge,
		gst_amount= gst_amount,
		gst_inc= gst_inc,
		transaction= transac_instance.id,
		invoice= invoice_instance,
	)

	invoice_item_instance.save()

	return JsonResponse({"data": "invoice saved", "invoice_id": invoice_item_instance.id})

# def getApplicationStatus(request):
# 	headers = {
# 			'FROM_ADMIN': 'Yes'
# 			}
	
# 	app_id = request.GET.get('id', None)

# 	if app_id == None:
# 		return JsonResponse({"data": "Invalid Application ID"})
# 	if app_id == '':
# 		return JsonResponse({"data": "Request need application ID"})
		
# 	datapdf = requests.get(url=f"{settings.API_URL}/application/check",params={"data":app_id}, stream=True,headers=headers)

# 	return JsonResponse({"data": json.loads(datapdf.text)})

def getApplicationStatus(request):
	
	app_id = request.GET.get('id', None)

	if app_id == None:
		return JsonResponse({"data": "Invalid Application ID"})
	if app_id == '':
		return JsonResponse({"data": "Request need application ID"})
		
	proxyDict = { 
              "http" :'10.23.131.81:3128',
			  "https":'10.23.131.81:3128'
            }
	response = requests.get(
        'https://api.sydneywater.com.au:443/propertyLinkInterface/applicationStatusCheck?applicationId='+app_id, 
		auth=('mark@hazlett.com.au', 'Haz_Ext_1'), proxies=proxyDict)

	if response.status_code != 200:
		return JsonResponse({"data": "Something Went Wrong", "status": response.status_code})

	return JsonResponse({"data": json.loads(response.text)})

def getlogsmail(request):
	headers = {
			'FROM_ADMIN': 'Yes'
			}
	datapdf = requests.get(url=f"{settings.API_URL}/email/logs",params={"data": datetime.now().strftime("%m-%d-%Y")}, stream=True,headers=headers)

	print(datapdf.text)
	return JsonResponse({"data": json.loads(datapdf.text)})

def emailLog(request):
	application_id = request.GET.get('application', None)
	if application_id == None or application_id == '':
		context =  {"status": False}
		return render(request, "users/email_logs.html", context)
	else:
		# application_id = application_id.replace("HAZPEXA",'')
		data = EmailLogs.objects.filter(application_id=application_id)
		context =  {"status": True, "data": data}
		return render(request, "users/email_logs.html", context)

def resetMailLog(request):
	application_id = request.GET.get('application', None)
	if application_id == None or application_id == '':
		return JsonResponse({"status": False, "message": "Invalid Application Id"})

	try:
		instance = EmailSendStatus.objects.get(application_id=application_id)
		instance.is_send = 0
		instance.save()
		return JsonResponse({"status": "Sending Email Again"})
	except Exception as e:
		raise e
		return JsonResponse({"status": False, "message": "Something went wrong"})


def resetDocumentStatus(request):
	application_id = request.GET.get('application', None)

	if application_id == None or application_id == '':
		return JsonResponse({"status": False, "message": "Invalid Application id"})
	
	try:
		instance = SwSearchMasterTbl.objects.get(applicationid=application_id)
		
		if instance.document_retrieval_tries < 400 and instance.product_status != 'Closed':
			return JsonResponse({"status": False, "message": "The System is Still checking for this document", "currentTries": instance.document_retrieval_tries})
		
		if instance.document_retrieval_tries > 400:
			instance.document_retrieval_tries = 400 - 10
		else:
			instance.document_retrieval_tries = instance.document_retrieval_tries - 10
			
		instance.product_status = 'In Progress'
		instance.save()

		return JsonResponse({"status": True, "message": "Checking for this document Again", "currentTries": instance.document_retrieval_tries})

	except Exception as e:
		raise e
		return JsonResponse({"status": False, "message": "Something went wrong"})


def viewEmail(request):

	paginator = Paginator(UserEmail.objects.all(), 25)

	username = request.GET.get('username', None)

	if username == None or username.strip() == '':
		paginator = Paginator(UserEmail.objects.all(), 25)
	else:
		paginator = Paginator(UserEmail.objects.filter(Q(username=username) | Q(first_name=username) | Q(last_name=username)), 25)

	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context =  {"data": page_obj}
	return render(request, "users/useremails.html", context)


def updateMail(request):

	email = request.POST.get("email", "")
	fname = request.POST.get("fname", None)
	lname = request.POST.get("lname", None)
	title = request.POST.get("title", None)
	user_id = request.POST.get("id", None)

	if user_id == None:
		return JsonResponse({"status": False, "message": "User Id Error"})

	try:
		instance = UserEmailDB.objects.get(id=user_id) 
	except Exception as e:
		return JsonResponse({"status": False, "message": "Email Instance Not found"})

	instance.first_name = fname
	instance.last_name = lname
	instance.email = email
	instance.title = title

	instance.save()

	return JsonResponse({"status": True, "message": "Email Updated Successfully"})


def external_payments(request):
	if request.user.is_superuser:
		if request.method == 'GET':
			# Get all records
			payments = InvoicePaymentExternal.objects.select_related('invoice')

			if len(payments):
				# Dates range object
				date_range = {
					"from_date": payments.first().payment_date.date(),
					"to_date": payments.last().payment_date.date()
				}

				data = []
				# List of required invoice ids
				invoiceid_list = payments.values_list('invoice', flat=True)

				invoice_queryset = SwInvoiceExternal.objects.filter(id__in=invoiceid_list)
				for payment in payments:
					invoice_data = invoice_queryset.filter(id=payment.invoice.id)

					new_amount = invoice_data[0].total_price - invoice_data[0].gst_charge

					new_data = {
						"payment_date": payment.payment_date.date(),
						"type": payment.payment_method,
						"amount": round(new_amount,2),
						"gst": invoice_data[0].gst_charge,
						"total": invoice_data[0].total_price,
						"place_holder": ""
					}

					data.append(new_data)
			else:
				data = []
				date_range = {
					"from_date": datetime.now(),
					"to_date": datetime.now()
				}

			return render(request, "swexternal/external_payments.html", context={"data": data, "date_range": date_range})
		else:
			fromdate = request.POST.get('from', None)
			todate = request.POST.get("to", None)
			# Create dates object
			date_range = {
				"from_date": fromdate,
				"to_date": todate
			}
			# Get required data using the dates
			data = get_external_payments_by_date(fromdate, todate)

			return render(request, "swexternal/external_payments.html", context={"data": data, "date_range": date_range})
	else:
		return redirect("/users/login")

def companyEditView(request):
	context = {'data': Company.objects.all()}
	return render(request, 'users/editcompany.html', context)

def companyEditSave(request,pk):
	if request.method == 'GET':
		context = {'data': Company.objects.filter(companyindex=pk)}
		return render(request, 'users/compedit.html', context)
	else:
		data = request.POST.copy()
		data.pop('csrfmiddlewaretoken')
		data.pop('user-record')
		data.pop('compCode')
		instance = Company.objects.get(companyindex=pk)
		for x in data:
			if data[x] == '' or data[x] == 'None':
				setattr(instance, x.lower(), None)
			else:
				setattr(instance, x.lower(), data[x])
		instance.save()
		context = {'data': Company.objects.filter(companyindex=pk)}
		return render(request, 'users/compedit.html', context)

def companyDelete(request):
	try:
		pk = request.POST.get('id', None)
		if pk == None:
			return JsonResponse({"status": False, "message": "Something went wrong"})
		instance = Company.objects.get(companyindex=pk)
		instance.delete()
	except Exception as e:
		print(e)
		return JsonResponse({"status": False, "message": "Something went wrong"})

	return JsonResponse({"status": True, "message": "Company Deleted"})

def payloadView(request):
	try:
		haz_id = request.GET.get('id', None)
		app = request.GET.get('application', None)
		if haz_id == None:
			return render(request, 'products/payloads.html')
		
		if app != None:
			try:
				app = SwSearchMasterTbl.objects.get(applicationid = app)
				app = app.order_details
			except:
				app = ""
		else:
			app = ""
		instance = SwCustomerPayloadTbl.objects.filter(referencenumber = haz_id)
		context = {'data': instance, "data_ms": app}
		return render(request, 'products/payloads.html', context)
	except Exception as e:
		raise e

def appSelectorView(request):
	return render(request, 'users/appselector.html')