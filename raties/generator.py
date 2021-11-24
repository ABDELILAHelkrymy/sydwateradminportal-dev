from .models import *
from datetime import datetime , timedelta
from django.conf import settings
from django.utils import timezone
import pdfkit
import os
import shutil
from django.template.loader import render_to_string
import pytz
from os.path import normpath, basename

class Invoice:
    
    def __init__(self, *args, **kwargs):
        self.files_path = os.path.join(os.path.dirname(settings.BASE_DIR), "files")
        self.static_path = os.path.join(os.path.dirname(settings.BASE_DIR), "src", "static")
        self.src_path = os.path.join(os.path.dirname(settings.BASE_DIR), "src")
        self.templates_path = os.path.join(os.path.dirname(settings.BASE_DIR), "src", "templates")

    def update(self, *args, **kwargs):
        
        try:
            kwargs.get('id')
        except Exception as e:
            raise e

        invoice_items = InvoiceItems.objects.using("raties_db").filter(invoice=kwargs.get('id')).order_by('-date_ordered')
        invoice_obj = RatiesInvoice.objects.using("raties_db").get(id=kwargs.get('id'))
        company_code = invoice_obj.company_code


        invoice_instance = RatiesInvoice.objects.using("raties_db").get(id=kwargs.get('id'))
        invoice_from_date = invoice_instance.searches_from
        invoice_to_date = invoice_instance.searches_to

        total = 0
        gst_total = 0
        disb_total = 0
        charge_total = 0

        data = []
        for x in invoice_items:
            data.append({
                "username": "PEXA",
                "date_ordered": x.date_ordered.strftime("%Y-%m-%d"),
                "reference": x.reference,
                "product_code": x.request_id.CouncilName,
                "client_reference": x.request_id.id,
                "disb_charge": x.disb_charge,
                "gst": x.gst_amount,
                "disb_charge_gst": x.gst_inc,
                "date_closed": x.date_closed.strftime("%Y-%m-%d")
            })

            total = total + x.gst_inc
            gst_total = gst_total + x.gst_amount
            disb_total = disb_total + x.disb
            charge_total = charge_total + x.charge
            cpdiscount = 0
            total_disc = total * (0 / 100)

        total_disc = total - total_disc
        disb_charge =  disb_total + charge_total
        date_now = datetime.now().strftime('%M-%d-%y-%H-%M-%S')
        context = {
            "data": data,
            "start_date": invoice_from_date,
            "end_date": invoice_to_date,
            #"company_instance": company_instance,
            "invoice_instance": invoice_instance,
            "date_now": datetime.now().strftime('%B %d, %Y'),
            "total": round(total,2),
            "company_discount": cpdiscount,
            "total_after_discount": round(total_disc,2),
            "tax": round(gst_total,2),
            "real_total": round(total_disc,2),
            "disb_charge": disb_charge,
            "total_invoice": total,
            "sub_total": total - gst_total,

        }

        rendered = render_to_string('raties/update_template_external.html', context)

        with open('update-1.html',"w") as html:
            html.write(rendered)
            html.close()
        file_name = 'invoice-' + date_now + '.pdf'
        pdfkit.from_file('update-1.html', file_name)
        
        # Done to allow path split in windows also

        path, file_name_1 = os.path.split(os.path.abspath(str(invoice_instance.pdf_link)))
        last_folder = os.path.join(basename(normpath(path)), file_name)
        file_path = os.path.join(settings.INVOICE_FILE_DIR, last_folder)
        final_folder = path

        shutil.move(file_name, final_folder)
        invoice_instance.pdf_link = os.path.join(final_folder, file_name)
        invoice_instance.search_charge = disb_total
        invoice_instance.service_charge = charge_total
        invoice_instance.gst_charge = gst_total
        invoice_instance.total_price = round(total_disc,2)
        invoice_instance.save()

        return invoice_instance

