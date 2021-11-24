from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from user.models import CompanyExternal
from datetime import datetime
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DetailView, ListView, View
from lrs.models import *
from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse, JsonResponse,FileResponse
from django.conf import settings
import os
from os.path import normpath, basename
from raties.generator import Invoice as InGenerator
from bootstrap_modal_forms.generic import (BSModalCreateView,BSModalUpdateView,BSModalReadView,BSModalDeleteView)
from .forms import *
import uuid
from datetime import datetime , timedelta
from django.conf import settings
from django.utils import timezone
import pdfkit
import os, io
from django.template.loader import render_to_string
from os.path import normpath, basename
from raties.utility import *
from django.urls import reverse


def ratiesDocumentDetails(request,pk):
    if request.user.is_superuser:
        if request.method == 'GET':
            document = Payload.objects.using('raties_db').filter(file_id=pk)
            return render(request, 'raties/raties_transaction.html', context={"data": document, "doc_id":pk})
    else:
        return redirect("/users/login")


def ratiesDocument(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            transactions = Document.objects.using('raties_db').all()
            return render(request, 'raties/raties_document.html', context={"data": transactions})
        else:
            order_id = request.POST.get('order_id', None)
            print(order_id)
            data = Document.objects.filter(id=order_id).using('raties_db')
            return render(request, 'raties/raties_document.html', context={"data": data })
    else:
        return redirect("/users/login")


def ratiesTransaction(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            document = Payload.objects.using('raties_db').all()
            return render(request, 'raties/raties_transaction.html', context={"data": document})
        else:
                transaction_id = request.POST.get('order_id', None)
                print(transaction_id)
                data = Payload.objects.filter(id=transaction_id).using('raties_db')
                return render(request, 'raties/raties_transaction.html', context={"data": data })
    else:
        return redirect("/users/login")


def ratiesTransactionDetails(request, pk):
    if request.user.is_superuser:
        if request.method == 'GET':
            property_obj = Payload.objects.using('raties_db').get(id=pk)
            return render(request, 'raties/raties_transaction_details.html', context={"data": property_obj})
    else:
        return redirect("/users/login")





class ratiesClientPayloadDetails(FormView):
    template_name = 'raties/payload_details.html'
    success_url = '/raties/product'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('raties:raties_client_payload_details', kwargs={'pk': self.kwargs['pk']})
    def form_valid(self, form):
        comment = form.cleaned_data['comment']
        CommentTable.objects.using("raties_db").create(comment=comment,payload=Payload(self.kwargs['pk']))
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ratiesClientPayloadDetails, self).get_context_data(*args, **kwargs)
        payload = Payload.objects.using('raties_db').get(id=self.kwargs['pk'])
        context['data'] = payload
        return context

def ratiesInvoicing(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            data = RatiesInvoice.objects.using("raties_db").all().order_by('-id')
            return render(request, "raties/raties_invoice.html", context={"data": data})
        else:
            fromdate = request.POST.get('from', None)
            todate = request.POST.get("to", None)

            if fromdate == None:
                data = RatiesInvoice.objects.using("raties_db").filter(searches_to=todate).order_by('-id')
            if todate == None:
                data = RatiesInvoice.objects.using("raties_db").filter(searches_from=fromdate).order_by('-id')

            if todate == None and fromdate == None:
                data = RatiesInvoice.objects.using("raties_db").all().order_by('-id')

            if todate != None and fromdate != None:
                data = RatiesInvoice.objects.using("raties_db").filter(searches_to=todate, searches_from=fromdate).order_by('-id')

            return render(request, "raties/raties_invoice.html", context={"data": data})
    else:
        return redirect("/users/login")


def getRatiesInvoiceStatus(request):
    invoice_id = request.GET.get('id', None)

    invoice_id = RatiesInvoice.objects.using("raties_db").get(id=invoice_id)
    count  = RatiesInvoicePayment.objects.using("raties_db").filter(invoice=invoice_id.id).count()

    if count > 0:
        return JsonResponse({"data": count, "items": list(RatiesInvoicePayment.objects.using("raties_db").filter(invoice=invoice_id).values())})
    return JsonResponse({"data": count})


def setRatiesInvoicePaid(request):
    invoice_id = request.POST.get('id', None)
    paymentMethod = request.POST.get('paymentMethod', None)
    date = request.POST.get('date', None)

    if invoice_id == None or paymentMethod == None:
        return JsonResponse({"message": "Empty Fields", "status": False})

    try:
        invoice_id = RatiesInvoice.objects.using("raties_db").get(id=invoice_id)

    except:
        return JsonResponse({"message": "Something went wrong", "status": False})
    payment_instance = RatiesInvoicePayment.objects.using("raties_db").create(
        is_paid=True,
        payment_method=paymentMethod,
        invoice=invoice_id
    )

    invoice_id.payment_status = 'Paid'
    invoice_id.save()
    payment_instance.save()

    return JsonResponse({"message": "Payment Recorded", "status": True, "invoice_id": invoice_id.id})

def setRatiesUnpaidInvoice(request):
    invoice_id = request.POST.get("id", None)

    if invoice_id == None:
        return JsonResponse({"message": "Empty Fields", "status": False})

    try:
        invoice_id = RatiesInvoice.objects.using("raties_db").get(id=invoice_id)

    except:
        return JsonResponse({"message": "Something went wrong", "status": False})

    invoice_id.payment_status = 'Unpaid'
    invoice_id.save()

    try:
        payment_instance = RatiesInvoicePayment.objects.using("raties_db").get(invoice=invoice_id)
    except:
        return JsonResponse({"message": "Something went wrong", "status": False})

    payment_instance.delete()

    return JsonResponse({"message": "Payment Recorded", "status": True, "invoice_id": invoice_id.id})


def ratiesManualCreation(request):
    if request.method == 'GET':
        invoice_id = request.GET.get('in')
        data = InvoiceItems.objects.using("raties_db").filter(invoice=invoice_id)
        return render(request, "raties/raties_invoice_create.html", context={ "data": data,  "invoice_id":invoice_id,"LRS_INVOICING_URL":settings.LRS_INVOICING_URL})


def ratiesRemoveInvoice(request):
    in_id = request.POST.get('id', None)
    invoice = InvoiceItems.objects.using("raties_db").get(id=in_id)
    invoice.delete()
    return JsonResponse({"success": True})


def ratiesAddInvoiceItem(request):
    username = request.POST.get("username", None)
    date_ordered = request.POST.get("date_ordered", None)
    date_completed = request.POST.get("date_completed", None)
    reference = request.POST.get("reference", None)
    client_reference = request.POST.get("client", None)
    invoice_id = request.POST.get("invoice_id", None)
    request_id = request.POST.get("request_id", None)
    disb = request.POST.get("disb")
    charge = request.POST.get("charge")
    gst = request.POST.get("gst")
    disb_charge = float(disb) + float(charge)
    gst_inc = float(gst) + disb_charge

    invoice_instance = RatiesInvoice.objects.using("raties_db").get(id=invoice_id)
    request_instance = Payload.objects.using("raties_db").get(id=request_id)
    last_item = InvoiceItems.objects.using("raties_db").filter(invoice=invoice_instance.id).order_by('count').last()

    instance = InvoiceItems.objects.using("raties_db").create(
        count=last_item.count + 1,
        username=username,
        date_ordered=date_ordered,
        date_closed = date_completed,
        reference=reference,
        client_reference=client_reference,
        disb=disb,
        charge=charge,
        disb_charge=disb_charge,
        gst_amount=gst,
        gst_inc=gst_inc,
        include=1,
        request_id=request_instance,
        invoice=invoice_instance
    )
    instance.save()

    return JsonResponse({
        "username": instance.username,
        "date_ordered": instance.date_ordered,
        "reference": "LRS Search",
        "client_reference": instance.client_reference,
        "disb": str(disb),
        "charge": str(charge),
        "gst": str(gst),
        "total": str(disb_charge),
        "gst_total": str(gst_inc),
        "count": str(instance.count),
        "id": instance.id
    })


def getInvoiceFile(request):

    invoice_id = request.GET.get("id",None)
    if invoice_id == None:
        return JsonResponse({"message": "File not Found"})
    file = RatiesInvoice.objects.using("raties_db").get(id=invoice_id)
    path, file_name = os.path.split(os.path.abspath(str(file.pdf_link)))
    last_folder = os.path.join( basename(normpath(path)), file_name)
    file_path = os.path.join(settings.INVOICE_FILE_DIR,last_folder)

    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')


def invoiceGenerate(request):
    invoice_id = request.GET.get('id', None)
    if invoice_id == None or invoice_id == '':
        return JsonResponse({"message": "Invalid Invoice ID Passed"})

    generator = InGenerator()
    res = generator.update(id=invoice_id)
    return redirect(f"/raties/invoice/file_download?id={invoice_id}")

def GroupServiceChargesView(request):
    if request.user.is_superuser:
        data = ServiceCharge.objects.using("raties_db").all()
        context={
        'data': data,
        }
        return render(request,'raties/raties_service_charge.html',context)
    else:
        return redirect("/users/login")
#
class GroupServiceChargesCreateView(FormView):
    template_name = 'raties/raties_service_charge_create.html'
    success_url 	= '/raties/service'
    form_class = ServiceChargesCreateForm

    def get_initial(self):
        initial = super().get_initial()
        initial['council_fee'] = 0
        initial['hazlett_fee'] =0
        initial['gst'] = 0
        initial['total'] = 0
        return initial

    def get_form_kwargs(self):
        kwargs = super(GroupServiceChargesCreateView, self).get_form_kwargs()
        council_obj = AuthCouncilPexaTable.objects.using("raties_db").all().values_list("AuthNo","Auth")
        kwargs['council_id'] =council_obj
        print(council_obj)
        product_obj = Product.objects.using("raties_db").all().values_list("id", "product_name")
        kwargs['product_id'] = product_obj
        return kwargs

    def form_valid(self, form):
        council_id =  form.cleaned_data['council_id']
        product_id = form.cleaned_data['product_id']
        council_fee = form.cleaned_data['council_fee']
        hazlett_fee = form.cleaned_data['hazlett_fee']
        gst = form.cleaned_data['gst']
        gst_enable = form.cleaned_data['gst_enable']
        total = form.cleaned_data['total']
        ServiceCharge.objects.using("raties_db").create(council_id=AuthCouncilPexaTable(council_id),product_id=Product(product_id),council_fee=council_fee,hazlett_fee=hazlett_fee,gst=gst,gst_enable=gst_enable,total=total)

        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(GroupServiceChargesCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = "Product Price Update"
        return context


def ratiesRemoveServiceCharge(request):
    id = request.POST.get('id', None)
    ServiceCharge.objects.using("raties_db").filter(id=id).delete()
    return JsonResponse({"success": True})
#
class ratiesUpdateServiceCharge(FormView):
    template_name = 'raties/raties_service_charge_create.html'
    success_url 	= '../../pricing'
    form_class = ServiceChargesCreateForm

    def get_form_kwargs(self):
        kwargs = super(ratiesUpdateServiceCharge, self).get_form_kwargs()
        council_obj = AuthCouncilPexaTable.objects.using("raties_db").all().values_list("AuthNo", "Auth")
        kwargs['council_id'] = council_obj
        product_obj = Product.objects.using("raties_db").all().values_list("id", "product_name")
        kwargs['product_id'] = product_obj
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        data = ServiceCharge.objects.using("raties_db").get(id=self.kwargs['id'])
        initial['council_id'] = data.council_id.AuthNo
        initial['product_id'] =  data.product_id.id
        initial['council_fee'] = data.council_fee
        initial['hazlett_fee'] = data.hazlett_fee
        initial['gst'] = data.gst
        initial['gst_enable'] =  data.gst_enable
        initial['total'] = data.total
        return initial

    def post(self,*args,**kwargs):
        council_id=self.request.POST['council_id']
        product_id = self.request.POST['product_id']
        council_fee=self.request.POST['council_fee']
        hazlett_fee = self.request.POST['hazlett_fee']
        gst=self.request.POST['gst']
        gst_enable = self.request.POST['gst_enable']
        total = self.request.POST['total']
        ServiceCharge.objects.using("raties_db").filter(id=self.kwargs['id']).update(council_id = council_id,product_id = product_id,council_fee = council_fee,hazlett_fee =  hazlett_fee,gst =  gst,gst_enable=gst_enable,total=total)
        return redirect('/raties/service')

    def get_context_data(self, *args, **kwargs):
        context = super(ratiesUpdateServiceCharge, self).get_context_data(*args, **kwargs)
        return context


def AuthCouncil(request):
    if request.user.is_superuser:
        data = AuthCouncilPexaTable.objects.using("raties_db").filter(CouncilFlag = 1).exclude(StatusUpdate=3)
        context={
        'data': data,
        }
        return render(request,'raties/raties_auth_council.html',context)
    else:
        return redirect("/users/login")

def convert_boolean_value(value):
    if value:
        return 1
    else:
        return 0

def convert_boolean(value):
    if value == True :
        return 1
    else:
        return None

class AuthCouncilCreateView(FormView):
    template_name = 'raties/raties_auth_council_create.html'
    success_url = '/raties/authcouncil'
    form_class = AuthCouncilCreateForm

    def form_valid(self, form):
        AuthNo = AuthCouncilPexaTable.objects.using("raties_db").latest('AuthNo').AuthNo + 1
        Auth = form.cleaned_data['Auth']
        AuthDX = form.cleaned_data['AuthDx']
        AuthSuburb = form.cleaned_data['AuthSuburb']
        AuthPostCode =form.cleaned_data['AuthPostCode']
        AuthPhoneNumber =form.cleaned_data['AuthPhoneNumber']
        CostDrainageDiag =form.cleaned_data['CostDrainageDiag']
        Cost149 =form.cleaned_data['Cost149']
        Cost1492 =form.cleaned_data['Cost1492']
        Cost1495 =form.cleaned_data['Cost1495']
        Cost603 =form.cleaned_data['Cost603']
        CostNoxiousWeed = form.cleaned_data['CostNoxiousWeed']
        CostWaterRates =form.cleaned_data['CostWaterRates']
        GSTCost603 = form.cleaned_data['GSTCost603']
        GSTCost1492 = form.cleaned_data['GSTCost1492']
        GSTCost149 = form.cleaned_data['GSTCost149']
        GSTCost1495 = form.cleaned_data['GSTCost1495']
        GSTCostDrainageDiag = form.cleaned_data['GSTCostDrainageDiag']
        GSTCostNoxiousWeed = form.cleaned_data['GSTCostNoxiousWeed']
        GSTCostWaterRates = form.cleaned_data['GSTCostWaterRates']
        GSTCostMisc = form.cleaned_data['GSTCostMisc']
        GSTEnabledCost603 = convert_boolean_value(form.cleaned_data['GSTEnabledCost603'])
        GSTEnabledCost1492 = convert_boolean_value(form.cleaned_data['GSTEnabledCost1492'])
        GSTEnabledCost1495 = convert_boolean_value(form.cleaned_data['GSTEnabledCost1495'])
        GSTEnabledCost149 = convert_boolean_value(form.cleaned_data['GSTEnabledCost149'])
        GSTEnabledCostDrainageDiag = convert_boolean_value(form.cleaned_data['GSTEnabledCostDrainageDiag'])
        GSTEnabledCostNoxiousWeed = convert_boolean_value(form.cleaned_data['GSTEnabledCostNoxiousWeed'])
        GSTEnabledCostWaterRates = convert_boolean_value(form.cleaned_data['GSTEnabledCostWaterRates'])
        GSTEnabledCostMisc = convert_boolean_value(form.cleaned_data['GSTEnabledCostMisc'])
        CouncilFlag = 1
        CostMisc = form.cleaned_data['CostMisc']
        msrepl_tran_version = uuid.uuid4()
        AuthCouncilPexaTable.objects.using("raties_db").create(AuthNo = AuthNo,Auth = Auth,AuthDX = AuthDX,AuthSuburb = AuthSuburb,AuthPostCode = AuthPostCode,AuthPhoneNumber = AuthPhoneNumber,CostDrainageDiag = CostDrainageDiag,Cost149 = Cost149,Cost1492 = Cost1492,Cost1495 = Cost1495,Cost603 = Cost603,CostNoxiousWeed = CostNoxiousWeed,CostWaterRates = CostWaterRates,GSTCost603 = GSTCost603,GSTCost1492 = GSTCost1492,GSTCost149 = GSTCost149,GSTCost1495 = GSTCost1495,GSTCostDrainageDiag = GSTCostDrainageDiag,GSTCostNoxiousWeed = GSTCostNoxiousWeed,GSTCostWaterRates = GSTCostWaterRates,GSTCostMisc = GSTCostMisc,GSTEnabledCost603 = GSTEnabledCost603,GSTEnabledCost1492 = GSTEnabledCost1492,GSTEnabledCost1495 = GSTEnabledCost1495,GSTEnabledCost149 = GSTEnabledCost149,GSTEnabledCostDrainageDiag = GSTEnabledCostDrainageDiag,GSTEnabledCostNoxiousWeed = GSTEnabledCostNoxiousWeed,GSTEnabledCostWaterRates = GSTEnabledCostWaterRates,GSTEnabledCostMisc = GSTEnabledCostMisc,CouncilFlag = CouncilFlag,CostMisc = CostMisc,msrepl_tran_version = msrepl_tran_version,LastUpdated = datetime.now(),EnableUpdate = 1,StatusUpdate = 1)

        return super().form_valid(form)

def defaule_val_n(val):
    if val:
        return val
    else :
        return 0

def defaule_val_check(val):
    if val:
        return val
    else :
        return None

class AuthCouncilUpdateView(FormView):
    template_name = 'raties/raties_auth_council_create.html'
    success_url 	= '../../pricing'
    form_class = AuthCouncilCreateForm

    def get_initial(self):
        initial = super().get_initial()
        data = AuthCouncilPexaTable.objects.using("raties_db").get(RecordIndex = self.kwargs['id'])
        initial['Auth'] = data.Auth
        initial['AuthDx'] = data.AuthDX
        initial['AuthSuburb'] = data.AuthSuburb
        initial['AuthPostCode'] = data.AuthPostCode
        initial['AuthPhoneNumber'] = data.AuthPhoneNumber
        initial['CostDrainageDiag'] = data.CostDrainageDiag
        initial['Cost149'] = data.Cost149
        initial['Cost1492'] = data.Cost1492
        initial['Cost1495'] = data.Cost1495
        initial['Cost603'] = data.Cost603
        initial['CostNoxiousWeed'] = data.CostNoxiousWeed
        initial['CostWaterRates'] = data.CostWaterRates
        initial['GSTCost603'] = data.GSTCost603
        initial['GSTCost1492'] = data.GSTCost1492
        initial['GSTCost149'] = data.GSTCost149
        initial['GSTCost1495'] = data.GSTCost1495
        initial['GSTCostDrainageDiag'] = data.GSTCostDrainageDiag
        initial['GSTCostNoxiousWeed'] = data.GSTCostNoxiousWeed
        initial['GSTCostWaterRates'] = data.GSTCostWaterRates
        initial['GSTCostMisc'] = data.GSTCostMisc
        initial['GSTEnabledCost603'] = defaule_val_check(data.GSTEnabledCost603)
        initial['GSTEnabledCost1492'] = defaule_val_check(data.GSTEnabledCost1492)
        initial['GSTEnabledCost1495'] = defaule_val_check(data.GSTEnabledCost1495)
        initial['GSTEnabledCost149'] = defaule_val_check(data.GSTEnabledCost149)
        initial['GSTEnabledCostDrainageDiag'] = defaule_val_check(data.GSTEnabledCostDrainageDiag)
        initial['GSTEnabledCostNoxiousWeed'] = defaule_val_check(data.GSTEnabledCostNoxiousWeed)
        initial['GSTEnabledCostWaterRates'] = defaule_val_check(data.GSTEnabledCostWaterRates)
        initial['GSTEnabledCostMisc'] = defaule_val_check(data.GSTEnabledCostMisc)
        initial['CostMisc'] = data.CostMisc
        print("aaaaaaaaaaaaa")
        print(data.GSTEnabledCost1495)

        return initial


    def post(self,*args,**kwargs):
        print(self.request.POST)
        Auth = self.request.POST['Auth']
        AuthDX = self.request.POST['AuthDx']
        AuthSuburb = self.request.POST['AuthSuburb']
        AuthPostCode = self.request.POST['AuthPostCode']
        AuthPhoneNumber = self.request.POST['AuthPhoneNumber']
        if 'CostDrainageDiag' in self.request.POST:
            CostDrainageDiag = self.request.POST['CostDrainageDiag']
        else:
            CostDrainageDiag = None
        Cost149 = defaule_val_n(self.request.POST['Cost149'])
        Cost1492 = defaule_val_n(self.request.POST['Cost1492'])
        Cost1495 = defaule_val_n(self.request.POST['Cost1495'])
        Cost603 = defaule_val_n(self.request.POST['Cost603'])
        CostNoxiousWeed = defaule_val_n(self.request.POST['CostNoxiousWeed'])
        CostWaterRates = defaule_val_n(self.request.POST['CostWaterRates'])
        GSTCost603 = defaule_val_n(self.request.POST['GSTCost603'])
        GSTCost1492 =defaule_val_n( self.request.POST['GSTCost1492'])
        GSTCost149 = defaule_val_n(self.request.POST['GSTCost149'])
        GSTCost1495 = defaule_val_n(self.request.POST['GSTCost1495'])
        if 'GSTCostDrainageDiag' in self.request.POST:
            GSTCostDrainageDiag = self.request.POST['GSTCostDrainageDiag']
        else:
            GSTCostDrainageDiag = None

        GSTCostNoxiousWeed = defaule_val_n(self.request.POST['GSTCostNoxiousWeed'])
        GSTCostWaterRates = defaule_val_n(self.request.POST['GSTCostWaterRates'])
        GSTCostMisc = defaule_val_n(self.request.POST['GSTCostMisc'])
        if 'GSTEnabledCost603' in self.request.POST:
            GSTEnabledCost603 = convert_boolean_value(self.request.POST['GSTEnabledCost603'])
        else:
            GSTEnabledCost603 = None

        if 'GSTEnabledCost1492' in self.request.POST:
            GSTEnabledCost1492 = convert_boolean_value(self.request.POST['GSTEnabledCost1492'])
        else:
            GSTEnabledCost1492 = None

        if 'GSTEnabledCost1495' in self.request.POST:
            GSTEnabledCost1495 = convert_boolean_value(self.request.POST['GSTEnabledCost1495'])
        else:
            GSTEnabledCost1495 = None

        if 'GSTEnabledCost149' in self.request.POST:
            GSTEnabledCost149 = convert_boolean_value(self.request.POST['GSTEnabledCost149'])
        else:
            GSTEnabledCost149 = None

        if 'GSTEnabledCostDrainageDiag' in self.request.POST:
            GSTEnabledCostDrainageDiag = convert_boolean_value(self.request.POST['GSTEnabledCostDrainageDiag'])
        else:
            GSTEnabledCostDrainageDiag = None


        if 'GSTEnabledCostNoxiousWeed' in self.request.POST:
            GSTEnabledCostNoxiousWeed = convert_boolean_value(self.request.POST['GSTEnabledCostNoxiousWeed'])
        else:
            GSTEnabledCostNoxiousWeed = None


        if 'GSTEnabledCostWaterRates' in self.request.POST:
            GSTEnabledCostWaterRates = convert_boolean_value(self.request.POST['GSTEnabledCostWaterRates'])
        else:
            GSTEnabledCostWaterRates = None

        if 'GSTEnabledCostMisc' in self.request.POST:
            GSTEnabledCostMisc = convert_boolean_value(self.request.POST['GSTEnabledCostMisc'])
        else:
            GSTEnabledCostMisc = None

        CostMisc = defaule_val_n(self.request.POST['CostMisc'])

        AuthCouncilPexaTable.objects.using("raties_db").filter(RecordIndex=self.kwargs['id']).update( Auth= Auth,AuthDX= AuthDX,AuthSuburb= AuthSuburb,AuthPostCode= AuthPostCode,AuthPhoneNumber= AuthPhoneNumber,CostDrainageDiag= CostDrainageDiag,Cost149= Cost149,Cost1492= Cost1492,Cost1495= Cost1495,Cost603= Cost603,CostNoxiousWeed= CostNoxiousWeed,CostWaterRates= CostWaterRates,GSTCost603= GSTCost603,GSTCost1492= GSTCost1492,GSTCost149= GSTCost149,GSTCost1495= GSTCost1495,GSTCostDrainageDiag= GSTCostDrainageDiag,GSTCostNoxiousWeed= GSTCostNoxiousWeed,GSTCostWaterRates= GSTCostWaterRates,GSTCostMisc= GSTCostMisc,GSTEnabledCost603= GSTEnabledCost603,GSTEnabledCost1492= GSTEnabledCost1492,GSTEnabledCost1495= GSTEnabledCost1495,GSTEnabledCost149= GSTEnabledCost149,GSTEnabledCostDrainageDiag= GSTEnabledCostDrainageDiag,GSTEnabledCostNoxiousWeed= GSTEnabledCostNoxiousWeed,GSTEnabledCostWaterRates= GSTEnabledCostWaterRates,GSTEnabledCostMisc= GSTEnabledCostMisc,CostMisc= CostMisc,LastUpdated=datetime.now(),EnableUpdate=1, StatusUpdate=2)
        return redirect('/raties/authcouncil')

    def get_context_data(self, *args, **kwargs):
        context = super(AuthCouncilUpdateView, self).get_context_data(*args, **kwargs)
        return context


def AuthCouncilRemove(request):
    id = request.POST.get('id', None)
    #sql = f"delete from AuthCouncilTable where RecordIndex = {id}"
    #out_put = ExecuteMSSQLCustomerQuery("HazEnquiries", sql).output
    AuthCouncilPexaTable.objects.using("raties_db").filter(RecordIndex=id).update(LastUpdated=datetime.now(),
                                                                                  EnableUpdate=1, StatusUpdate=3)
    #AuthCouncilPexaTable.objects.using("raties_db").filter(RecordIndex = id).delete()
    return JsonResponse({"success": True})


def reset_raties_db(request):
    Document.objects.using("raties_db").all().delete()
    RatiesInvoice.objects.using("raties_db").all().delete()
    PropertyEnquiryFormTable.objects.using("raties_db").all().delete()
    AuthRequestsTable.objects.using("raties_db").all().delete()
    Payload.objects.using("raties_db").all().delete()
    return redirect("/raties/transaction")


def Authority(request):
    if request.user.is_superuser:
        data = AuthCouncilPexaTable.objects.using("raties_db").all().exclude(StatusUpdate=3)
        context={
        'data': data,
        }
        return render(request,'raties/raties_authority.html',context)
    else:
        return redirect("/users/login")


class AuthorityCreateView(FormView):
    template_name = 'raties/raties_authority_create.html'
    success_url = '/raties/authority'
    form_class = AuthorityCreateForm

    def form_valid(self, form):
        try:
            RecordIndex = AuthCouncilPexaTable.objects.using("raties_db").latest('RecordIndex').RecordIndex +1
        except:
            RecordIndex = 1
        Auth = form.cleaned_data['Auth']
        AuthDX = form.cleaned_data['AuthDx']
        AuthSuburb = form.cleaned_data['AuthSuburb']
        AuthPostCode =form.cleaned_data['AuthPostCode']
        AuthPhoneNumber =form.cleaned_data['AuthPhoneNumber']
        AuthMiscellanous =convert_boolean_value(form.cleaned_data['AuthMiscellanous'])
        EnquiryCost =form.cleaned_data['EnquiryCost']
        EnquiryGSTAmount =form.cleaned_data['EnquiryGSTAmount']
        EnquiryGSTReq =convert_boolean_value(form.cleaned_data['EnquiryGSTReq'])
        CouncilFlag = 0
        msrepl_tran_version = uuid.uuid4()
        AuthCouncilPexaTable.objects.using("raties_db").create(RecordIndex=RecordIndex,Auth=Auth,AuthDX=AuthDX,AuthSuburb=AuthSuburb,AuthPostCode=AuthPostCode,AuthPhoneNumber=AuthPhoneNumber,AuthMiscellanous=AuthMiscellanous,EnquiryCost=EnquiryCost,EnquiryGSTAmount=EnquiryGSTAmount,EnquiryGSTReq=EnquiryGSTReq,CouncilFlag=CouncilFlag,msrepl_tran_version=msrepl_tran_version,LastUpdated = datetime.now(),EnableUpdate = 1,StatusUpdate = 1)
        return super().form_valid(form)


class AuthorityUpdateView(FormView):
    template_name = 'raties/raties_authority_create.html'
    success_url 	= '../../pricing'
    form_class = AuthorityCreateForm

    def get_initial(self):
        initial = super().get_initial()

        data = AuthCouncilPexaTable.objects.using("raties_db").get(RecordIndex=self.kwargs['id'])
        initial['Auth'] = data.Auth
        initial['AuthDx'] =  data.AuthDX
        initial['AuthSuburb'] = data.AuthSuburb
        initial['AuthPostCode'] =  data.AuthPostCode
        initial['AuthPhoneNumber'] =  data.AuthPhoneNumber
        initial['AuthMiscellanous'] =  defaule_val_check(data.AuthMiscellanous)
        initial['EnquiryCost'] =  data.EnquiryCost
        initial['EnquiryGSTAmount'] =  data.EnquiryGSTAmount
        initial['EnquiryGSTReq'] =  defaule_val_check(data.EnquiryGSTReq)
        print(data.AuthMiscellanous)
        print(data.EnquiryGSTReq)

        return initial


    def post(self,*args,**kwargs):
        print(self.request.POST)
        Auth = self.request.POST['Auth']
        AuthDX = self.request.POST['AuthDx']
        AuthSuburb = self.request.POST['AuthSuburb']
        AuthPostCode = self.request.POST['AuthPostCode']
        AuthPhoneNumber = self.request.POST['AuthPhoneNumber']
        if 'AuthMiscellanous' in self.request.POST:
            AuthMiscellanous = convert_boolean_value(self.request.POST['AuthMiscellanous'])
        else:
            AuthMiscellanous = None
        EnquiryCost = self.request.POST['EnquiryCost']
        EnquiryGSTAmount = self.request.POST['EnquiryGSTAmount']
        if 'EnquiryGSTReq' in self.request.POST:
            EnquiryGSTReq = convert_boolean_value(self.request.POST['EnquiryGSTReq'])
        else:
            EnquiryGSTReq = None

        AuthCouncilPexaTable.objects.using("raties_db").filter(RecordIndex=self.kwargs['id']).update(Auth=Auth ,AuthDX=AuthDX ,AuthSuburb=AuthSuburb ,AuthPostCode=AuthPostCode ,AuthPhoneNumber=AuthPhoneNumber ,AuthMiscellanous=AuthMiscellanous ,EnquiryCost=EnquiryCost ,EnquiryGSTAmount=EnquiryGSTAmount ,EnquiryGSTReq=EnquiryGSTReq,LastUpdated = datetime.now(),EnableUpdate = 1,StatusUpdate = 2)
        return redirect('/raties/authority')

    def get_context_data(self, *args, **kwargs):
        context = super(AuthorityUpdateView, self).get_context_data(*args, **kwargs)
        return context


def AuthorityRemove(request):
    id = request.POST.get('id', None)
    AuthCouncilPexaTable.objects.using("raties_db").filter(RecordIndex=id).update(LastUpdated = datetime.now(),EnableUpdate = 1,StatusUpdate = 3)
    #AuthCouncilPexaTable.objects.using("raties_db").filter(RecordIndex=id).delete()
    return JsonResponse({"success": True})


def ratiesTemplate(request,id):
    if request.user.is_superuser:
        if request.method == 'GET':
            EnquiryForm = PropertyEnquiryFormTable.objects.using('raties_db').get(SetId = id)
            auth_request = AuthRequestsTable.objects.using('raties_db').filter(SetId= EnquiryForm.SetId)

            for auth_request_ in auth_request:
                print(auth_request_.AuthNo.Auth)
            context = {
                'EnquiryForm' : EnquiryForm,
                'auth': EnquiryForm.CouncilName,
                'DX': EnquiryForm.DX,
                'FromStreetAddress': EnquiryForm.FromStreetAddress,
                'auth_request' : auth_request
            }
            print(context)
            rendered = render_to_string('raties/raties_form_template.html', context)
            html_dir = f'{os.getenv("ADMIN_FORM_FOLDER")}form_{EnquiryForm.SetId}.html'
            print(html_dir)
            with open(html_dir, "w") as html:
               html.write(rendered)
               html.close()


            file_name = f'form_{EnquiryForm.SetId}.pdf'
            options = {
            'page-size': 'letter',
            'margin-top': '0.0in',
            'margin-right': '0.0in',
            'margin-bottom': '0.0in',
            'margin-left': '0.0in'}

            pdf_dir =f'{os.getenv("ADMIN_FORM_FOLDER")}{file_name}'
            pdfkit.from_file(html_dir, pdf_dir, options = options)
            return FileResponse(open(pdf_dir, 'rb'), content_type='application/pdf')

        else:
            order_id = request.POST.get('order_id', None)
            data = RatiesSearch.objects.filter(orderid=order_id).using('raties_db')
            return render(request, 'raties/raties_home.html', context={"data": data})
    else:
        return redirect("/users/login")


def ratiesDownloadForm(request,id):
    response = HttpResponse(r'C:\Users\admin\PycharmProjects\sydwateradminportal-master@b65d2207c8a\test_john_invoice-.pdf', content_type='application/pdf')
    response['Content-Disposition'] = "inline"
    return response

    return



class ratiesDocumentUploadView(FormView):
    template_name = 'raties/raties_upload_file.html'
    form_class = DocumentFileUploadForm

    def form_valid(self, form_class):
        file_list = self.request.FILES.getlist('file_field')
        print(self.request.FILES)
        sftp = sftp_connection()
        sftp.cwd("data")
        for file in file_list:
            handle_uploaded_file(file)
            sftp.put('/home/centos/sydwateradminportal/media/document/'+file.name,"document/"+file.name)
            #os.remove('media/document/' + file.name)
        return redirect(reverse('raties:raties_document_details', kwargs={'pk': self.kwargs['pk']}))


    def get_context_data(self, *args, **kwargs):
        context = super(ratiesDocumentUploadView, self).get_context_data(*args, **kwargs)
        return context

def handle_uploaded_file(f):
    with open('/home/centos/sydwateradminportal/media/document/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def simple_upload(request,pk,id):
    if request.method == 'POST' and request.FILES['file_field']:
        doc_folder = os.getenv("SFTP_DOCUMENT")
        payload_obj = Payload.objects.using("raties_db").get(id=pk)
        counter = DocumentOutputTable.objects.using("raties_db").filter(client_ref=payload_obj.SearchID).count()
        file_name = payload_obj.SearchID
        number_str = str(counter+1)
        file_name += f"_{number_str.zfill(2)}.pdf"
        myfile = request.FILES['file_field']
        fs = FileSystemStorage()
        filename = fs.save(file_name, myfile)
        sftp = sftp_connection()
        folder = os.getenv("SFTP_FOLDER")
        sftp.cwd(folder)
        sftp.put('media/' + file_name, doc_folder+"/" + file_name)
        DocumentOutputTable.objects.using("raties_db").create(client_ref=payload_obj.SearchID, counter=counter + 1)
        return redirect(reverse('raties:raties_document_details', kwargs={'pk': pk}))
    return render(request, 'raties/raties_upload_file.html', context= {"form": DocumentFileUploadForm})

def transaction_upload(request,pk):
    payload_obj = Payload.objects.using("raties_db").get(id=pk)
    document_obj = DocumentOutputTable.objects.using("raties_db").filter(client_ref=payload_obj.SearchID)
    if request.method == 'POST' and request.FILES['file_field']:
        doc_folder  = os.getenv("SFTP_DOCUMENT")
        counter = document_obj.count()
        file_name = payload_obj.SearchID
        number_str = str(counter + 1)
        file_name += f"_{number_str.zfill(2)}.pdf"
        myfile = request.FILES['file_field']
        fs = FileSystemStorage()
        filename = fs.save(file_name, myfile)
        sftp = sftp_connection()
        folder = os.getenv("SFTP_FOLDER")
        sftp.cwd(folder)
        sftp.put('media/' + file_name, doc_folder+"/" + file_name)
        DocumentOutputTable.objects.using("raties_db").create(client_ref=payload_obj.SearchID, counter=counter + 1)
        return redirect(reverse('raties:raties_transaction'))
    return render(request, 'raties/raties_upload_file.html', context= {"form": DocumentFileUploadForm,"document_obj":document_obj})


def ProductView(request):
    #sql_script_for_raties()
    if request.user.is_superuser:
        data = Product.objects.using("raties_db").all()
        context={
        'data': data,
        }
        return render(request,'raties/raties_product.html',context)
    else:
        return redirect("/users/login")


class ProductCreateView(FormView):
    template_name = 'raties/raties_product_create.html'
    success_url = '/raties/product'
    form_class = ProductCreateForm

    def form_valid(self, form):
        product_name = form.cleaned_data['product_name']
        Product.objects.using("raties_db").create(product_name=product_name)
        return super().form_valid(form)


class ProductUpdateView(FormView):
    template_name = 'raties/raties_product_create.html'
    success_url = '/raties/product'
    form_class = ProductCreateForm

    def get_initial(self):
        initial = super().get_initial()
        data = Product.objects.using("raties_db").get(id=self.kwargs['id'])
        initial['product_name'] = data.product_name
        return initial

    def post(self,*args,**kwargs):
        product_name = self.request.POST['product_name']
        Product.objects.using("raties_db").filter(id=self.kwargs['id']).update(product_name=product_name)
        return redirect('/raties/product')

    def get_context_data(self, *args, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(*args, **kwargs)
        return context


def ProductRemoveView(request):
    id = request.POST.get('id', None)
    Product.objects.using("raties_db").filter(id=id).delete()
    return JsonResponse({"success": True})


def TransactionStatus(request,pk):
    if request.method == 'POST' :
        status = request.POST.get('status', None)
        print(status)
        payload_obj = Payload.objects.using("raties_db").get(id=pk)
        payload_obj.processed = status
        if payload_obj.processed == '3':
            payload_obj.completed_date = timezone.now()
        else:
            payload_obj.completed_date = None
        payload_obj.save()
        return redirect(reverse('raties:raties_transaction'))
    return render(request, 'raties/raties_status.html', context= {"form": PayloadStatusForm})

