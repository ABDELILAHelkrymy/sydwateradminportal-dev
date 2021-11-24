from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
import requests
from django.views.generic import CreateView, UpdateView, DetailView, ListView, View
from .forms import *
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from bootstrap_modal_forms.generic import (BSModalCreateView, BSModalUpdateView, BSModalReadView, BSModalDeleteView)
from .forms import DiscountCreateForm
from user.models import CompanyExternal
from datetime import datetime
from .utility import *

# Create your views here.

def lrsHome(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            records = request.GET.get('records', None)
            if records == "all":
                transactions = LrsSearchTransaction.objects.order_by('-jobid').all().using('hazlrs_db')
                print("all")
            else:
                transactions = LrsSearchTransaction.objects.filter(
                    orderdatetime__gte=monthdelta(datetime.today(), -3)).order_by('-jobid').all().using('hazlrs_db')
                print("else")
            payloads = LrsPayload.objects.all().using('hazlrs_db')
            payloads = set(payloads)

            for i in transactions:
                k = set(filter(lambda payload: payload.referenceNumber == i.orderid, payloads))
                payloads -= k
                i.payload = k

            return render(request, 'lrstemplates/lrs_home.html', context={"data": transactions})
        else:
            order_id = request.POST.get('order_id', None)
            data = LrsSearchTransaction.objects.filter(orderid=order_id).using('hazlrs_db')
            return render(request, 'lrstemplates/lrs_home.html', context={"data": data})
    else:
        return redirect("/users/login")


def lrsDocument(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            transactions = LrsSearchNotBilled.objects.all().order_by('-id').using('hazlrs_db')

            return render(request, 'lrstemplates/lrs_document.html', context={"data": transactions})

    else:
        return redirect("/users/login")


def lrsDownloadFile(request, file):
    url = f"{settings.HAZLRS_API_URL}/req/lrs/{file}.pdf"
    payload = {}
    headers = {
        'Authorization': f'Bearer {settings.LRS_TOKEN}'
    }
    print(url)
    print(settings.LRS_TOKEN)
    file = requests.get(url, headers=headers, data=payload, )
    response = HttpResponse(file.content, content_type='application/pdf')
    response['Content-Disposition'] = "inline"
    print(response)
    return response


class lrsPricingView(ListView):
    template_name = "lrstemplates/lrs_price.html"
    context_object_name = "product_pricing"

    def get_queryset(self):
        # return LrsProductPricing.objects.all().using('hazlrs_db')
        return LrsBillingCode.objects.all().using('hazlrs_db')

    def get_context_data(self, *args, **kwargs):
        context = super(lrsPricingView, self).get_context_data(**kwargs)
        products = LrsProductPricing.objects.all().using('hazlrs_db')
        billing_code = LrsProductPricing.objects.all().using('hazlrs_db')

        for a in products:
            total = a.product_price + a.lrs_product_fees
            if a.product_gst_fees == "Yes" and a.lrs_product_gst_fees == "Yes":
                messages.error(self.request, "Cannot check both GST on Services Fees and GST on Total")
            if a.product_gst_fees == "Yes":
                a.lrs_product_gst_fees = "No"
                a.save()
                total += (a.product_price * .10)
                print("productGtsFee")
            elif a.lrs_product_gst_fees == "Yes":
                a.product_gst_fees = "No"
                a.save()
                total += total / 10
                print("lrsProductGtsFee")

            a.total = total
            a.save()
        context['products'] = products
        context['billing_code'] = billing_code

        return context


class UpdateLrsProductView(FormView):
    template_name = 'lrstemplates/lrs_update_price.html'
    success_url = '../../pricing'
    form_class = PriceUpdateForm

    def get_initial(self):
        initial = super().get_initial()
        lrs_product = LrsProductPricing.objects.filter(pk=self.kwargs['pk']).using("hazlrs_db")
        for lrs_product_ in lrs_product:
            initial['product_price'] = lrs_product_.product_price
            initial['product_gst_fees'] = lrs_product_.product_gst_fees
            initial['lrs_product_fees'] = lrs_product_.lrs_product_fees
            initial['lrs_product_gst_fees'] = lrs_product_.lrs_product_gst_fees
        return initial

    def form_valid(self, form):
        LrsProductPricing.objects.filter(pk=self.kwargs['pk']).using("hazlrs_db").update(
            product_price=form.cleaned_data['product_price'],
            product_gst_fees=form.cleaned_data['product_gst_fees'],
            lrs_product_fees=form.cleaned_data['lrs_product_fees'],
            lrs_product_gst_fees=form.cleaned_data['lrs_product_gst_fees']
        )

        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(UpdateLrsProductView, self).get_context_data(*args, **kwargs)
        context['title'] = "Product Price Update"
        return context


class lrsInvoinceView(ListView):
    template_name = "lrstemplates/lrs_invoice.html"
    context_object_name = "lrs_invoice"

    def get_queryset(self):
        return LrsInvoice.objects.all().using('hazlrs_db')

    def get_context_data(self, *args, **kwargs):
        context = super(lrsInvoinceView, self).get_context_data(**kwargs)
        return context


def getLrsInvoiceStatus(request):
    invoice_id = request.GET.get('id', None)

    invoice_id = LrsInvoice.objects.using("hazlrs_db").get(id=invoice_id)
    count = LrsInvoicePayment.objects.using("hazlrs_db").filter(invoice=invoice_id.id).count()

    if count > 0:
        return JsonResponse({"data": count, "items": list(
            LrsInvoicePayment.objects.using("hazlrs_db").filter(invoice=invoice_id).values())})
    return JsonResponse({"data": count})


def setLrsInvoicePaid(request):
    invoice_id = request.POST.get('id', None)
    paymentMethod = request.POST.get('paymentMethod', None)
    date = request.POST.get('date', None)

    if invoice_id == None or paymentMethod == None:
        return JsonResponse({"message": "Empty Fields", "status": False})

    try:
        invoice_id = LrsInvoice.objects.using("hazlrs_db").get(id=invoice_id)

    except:
        return JsonResponse({"message": "Something went wrong", "status": False})
    payment_instance = LrsInvoicePayment.objects.using("hazlrs_db").create(
        is_paid=True,
        payment_method=paymentMethod,
        invoice=invoice_id
    )

    invoice_id.payment_status = 'Paid'
    invoice_id.save()
    payment_instance.save()

    return JsonResponse({"message": "Payment Recorded", "status": True, "invoice_id": invoice_id.id})


def setLrsUnpaidInvoice(request):
    invoice_id = request.POST.get("id", None)

    if invoice_id == None:
        return JsonResponse({"message": "Empty Fields", "status": False})

    try:
        invoice_id = LrsInvoice.objects.using("hazlrs_db").get(id=invoice_id)

    except:
        return JsonResponse({"message": "Something went wrong", "status": False})

    invoice_id.payment_status = 'Unpaid'
    invoice_id.save()

    try:
        payment_instance = LrsInvoicePayment.objects.using("hazlrs_db").get(invoice=invoice_id)
    except:
        return JsonResponse({"message": "Something went wrong", "status": False})

    payment_instance.delete()

    return JsonResponse({"message": "Payment Recorded", "status": True, "invoice_id": invoice_id.id})


def lrsManualCreation(request):
    if request.method == 'GET':
        # company_code = request.GET.get('id')
        invoice_id = request.GET.get('in')
        data = InvoiceItems.objects.using("hazlrs_db").filter(invoice=invoice_id)
        # transactions = LrsSearchTransaction.objects.using("hazlrs_db").filter(internal_username__contains=company_code + '+')
        # transactions = LrsSearchTransaction.objects.using("hazlrs_db").all()
        return render(request, "lrstemplates/lrs_invoice_create.html",
                      context={"data": data, "invoice_id": invoice_id, "LRS_INVOICING_URL": settings.LRS_INVOICING_URL})


def lrsRemoveInvoice(request):
    in_id = request.POST.get('id', None)
    invoice = InvoiceItems.objects.using("hazlrs_db").get(id=in_id)
    invoice.delete()
    return JsonResponse({"success": True})


def lrsAddInvoiceItem(request):
    username = request.POST.get("username", None)
    date_ordered = request.POST.get("date_ordered", None)
    date_completed = request.POST.get("date_completed", None)
    reference = request.POST.get("reference", None)
    client_reference = request.POST.get("client", None)
    invoice_id = request.POST.get("invoice_id", None)
    print(invoice_id)

    invoice_instance = LrsInvoice.objects.using("hazlrs_db").get(id=invoice_id)

    disb = request.POST.get("disb", 5.0)
    charge = request.POST.get("charge", 3.0)
    gst = request.POST.get("gst", 0.5)

    disb_charge = float(disb) + float(charge)

    gst_inc = float(gst) + disb_charge

    last_item = InvoiceItems.objects.using("hazlrs_db").filter(invoice=invoice_instance.id).order_by('count').last()

    instance = InvoiceItems.objects.using("hazlrs_db").create(
        count=last_item.count + 1,
        username=username,
        date_ordered=date_ordered,
        date_closed=date_completed,
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


def lrsInvoicing(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            data = LrsInvoice.objects.using("hazlrs_db").all().order_by('-id')
            return render(request, "lrstemplates/lrs_invoice.html", context={"data": data})
        else:
            fromdate = request.POST.get('from', None)
            todate = request.POST.get("to", None)

            if fromdate == None:
                data = LrsInvoice.objects.using("hazlrs_db").filter(searches_to=todate).order_by('-id')
            if todate == None:
                data = LrsInvoice.objects.using("hazlrs_db").filter(searches_from=fromdate).order_by('-id')

            if todate == None and fromdate == None:
                data = LrsInvoice.objects.using("hazlrs_db").all().order_by('-id')

            if todate != None and fromdate != None:
                data = LrsInvoice.objects.using("hazlrs_db").filter(searches_to=todate,
                                                                    searches_from=fromdate).order_by('-id')

            return render(request, "lrstemplates/lrs_invoice.html", context={"data": data})
    else:
        return redirect("/users/login")


def discount(request):
    if request.user.is_superuser:
        discount = LrsDiscountTbl.objects.using("hazlrs_db").all()
        company = CompanyExternal.objects.all().exclude(discount=None)
        context = {
            'discount': discount,
            'company': company
        }
        return render(request, 'lrstemplates/lrs_discount.html', context)
    else:
        return redirect("/users/login")


class DiscountCreateView(BSModalCreateView):
    print("LRS DiscountCreateView")
    form_class = DiscountCreateForm
    template_name = 'lrstemplates/lrs_create_discount.html'
    success_url = '../../lrs/discount'

    def form_valid(self, form):
        f = form.save(commit=False)
        print(form.cleaned_data['product_code'])
        if form.cleaned_data['product_code'] == "1":
            print("true")
            f.is_total = True
            f.product_code = None

        f.save(using='hazlrs_db')
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(DiscountCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = "Product Price Update"
        return context


class UpdateDiscountView(BSModalCreateView):
    template_name = 'lrstemplates/lrs_create_discount.html'
    success_url = '../../pricing'
    form_class = DiscountEditForm

    def get_initial(self):
        initial = super().get_initial()
        lrs_discount = LrsDiscountTbl.objects.using("hazlrs_db").get(id=self.kwargs['id'])
        initial['discount'] = lrs_discount.discount
        initial['product_code'] = lrs_discount.product_code
        if lrs_discount.is_percent:
            initial['is_percent'] = 1
        else:
            initial['is_percent'] = 0
        return initial

    def post(self, *args, **kwargs):
        discount = self.request.POST['discount']
        is_percent = self.request.POST['is_percent']
        discount_instance = LrsDiscountTbl.objects.using("hazlrs_db").filter(id=kwargs["id"])
        discount_instance.update(discount=float(discount), is_percent=is_percent)
        print("discount", discount)
        if discount_instance[0].is_total:
            messages.success(self.request,
                             "Edited Total Invoice to Discount " + str(discount) +
                             discount_instance[0].getSign())
        else:
            messages.success(self.request,
                             "Edited " + discount_instance[0].product_code + " to Discount " + str(discount) +
                             discount_instance[0].getSign())
        return redirect('/lrs/discount')

    def get_context_data(self, *args, **kwargs):
        context = super(UpdateDiscountView, self).get_context_data(*args, **kwargs)
        return context


def lrsRemoveDiscount(request):
    in_id = request.POST.get('id', None)
    invoice = LrsDiscountTbl.objects.using("hazlrs_db").get(id=in_id)
    invoice.delete()
    return JsonResponse({"success": True})


class lrsLogsView(FormView):
    template_name = 'lrstemplates/lrs_logs.html'
    success_url = '../../pricing'
    form_class = LogsForm

    def form_valid(self, form):
        logs = form.cleaned_data['logs']
        date = form.cleaned_data['date']
        date_text = ""
        if date:
            date_text = f"?date={date}"
        print("test")
        url = f"{settings.HAZLRS_API_URL}/req/lrs/log/{logs}{date_text}"
        print(url)
        payload = {}
        headers = {
            'Authorization': f'Bearer {settings.LRS_TOKEN}'
        }
        file = requests.get(url, headers=headers, data=payload, )
        print(file)
        response = HttpResponse(file.content, content_type='text/plain')
        response['Content-Disposition'] = "inline"
        print("test2")
        return response

    def get_context_data(self, *args, **kwargs):
        context = super(lrsLogsView, self).get_context_data(*args, **kwargs)
        context['title'] = "LRS logs"
        return context


def lrsLogsDetailsView(request, file):
    print("test")
    url = f"{settings.HAZLRS_API_URL}/req/lrs/log/{file}"
    payload = {}
    headers = {
        'Authorization': f'Bearer {settings.LRS_TOKEN}'
    }
    print("test1")
    print(url, payload, headers)
    file = requests.get(url, headers=headers, data=payload, )
    print(file)
    response = HttpResponse(file.content, content_type='text/plain')
    response['Content-Disposition'] = "inline"
    print("test2")
    return response


def payments(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            # Get all records
            payments = LrsInvoicePayment.objects.using('hazlrs_db').select_related('invoice')

            if len(payments):
                # Dates range object
                date_range = {
                    "from_date": payments.first().payment_date.date(),
                    "to_date": payments.last().payment_date.date()
                }

                data = []
                # List of required invoice ids
                invoiceid_list = payments.values_list('invoice', flat=True)
                invoice_queryset = LrsInvoice.objects.using('hazlrs_db').filter(id__in=invoiceid_list)
                for payment in payments:
                    invoice_data = invoice_queryset.filter(id=payment.invoice.id)

                    new_amount = invoice_data[0].total_price - invoice_data[0].gst_charge

                    new_data = {
                        "payment_date": payment.payment_date.date(),
                        "type": payment.payment_method,
                        "amount": round(new_amount, 2),
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

            return render(request, "lrstemplates/lrs_payments.html", context={"data": data, "date_range": date_range})
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

            return render(request, "lrstemplates/lrs_payments.html", context={"data": data, "date_range": date_range})
    else:
        return redirect("/users/login")


def get_payments_by_date(fromdate, todate):
    if fromdate == None:
        payments_queryset = LrsInvoicePayment.objects.using('hazlrs_db').select_related('invoice').filter(
            payment_date__range=(todate, todate))
    if todate == None:
        payments_queryset = LrsInvoicePayment.objects.using('hazlrs_db').select_related('invoice').filter(
            payment_date__range=(fromdate, fromdate))
    if todate == None and fromdate == None:
        payments_queryset = LrsInvoicePayment.objects.using('hazlrs_db').select_related('invoice')
    if todate != None and fromdate != None:
        payments_queryset = LrsInvoicePayment.objects.using('hazlrs_db').select_related('invoice').filter(
            payment_date__range=(fromdate, todate))

    data_array = []
    # List of required invoice ids

    invoiceid_list = payments_queryset.values_list('invoice', flat=True)
    invoice_queryset = LrsInvoice.objects.using('hazlrs_db').filter(id__in=invoiceid_list)

    for payment in payments_queryset:
        invoice_data = invoice_queryset.filter(id=payment.invoice.id)

        new_amount = invoice_data[0].total_price - invoice_data[0].gst_charge

        new_data = {
            "payment_date": payment.payment_date.date(),
            "type": payment.payment_method,
            "amount": round(new_amount, 2),
            "gst": invoice_data[0].gst_charge,
            "total": invoice_data[0].total_price,
            "place_holder": ""
        }

        data_array.append(new_data)

    return data_array


def payloadView(request):
    try:
        haz_id = request.GET.get('id', None)
        print(haz_id)
        try:
            lrs_search_object = LrsSearchTransaction.objects.using('hazlrs_db').get(jobid=haz_id)
        except:
            lrs_search_object = ""
        try:
            lrs_payload = LrsPayload.objects.using('hazlrs_db').get(
                orderId=lrs_search_object.orderid.replace("HAZPEXA", ""))
        except:
            lrs_payload = None
        try:
            lrs_response = LrsResponsePayload.objects.using('hazlrs_db').get(
                orderId=lrs_search_object.orderid.replace("HAZPEXA", ""))
        except:
            lrs_response = None

        context = {'data': lrs_search_object, "payload_obj": lrs_payload, "response_obj": lrs_response}
        return render(request, 'lrstemplates/lrs_payloads.html', context)
    except Exception as e:
        raise e


def lrsDocumentView(request):
    try:
        id = request.GET.get('id', None)
        print(id)
        try:
            lrs_search_object = LrsSearchNotBilled.objects.using('hazlrs_db').get(id=id)
        except:
            lrs_search_object = ""

        context = {'data': lrs_search_object}
        return render(request, 'lrstemplates/lrs_document_view.html', context)
    except Exception as e:
        raise e
