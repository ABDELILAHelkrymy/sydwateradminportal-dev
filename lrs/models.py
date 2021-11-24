from django.db import models
import random
import os
from django.utils import timezone

# Create your models here.
class LrsSearchTransaction(models.Model):
    jobid = models.AutoField(db_column='job_id', primary_key=True)
    orderid = models.CharField(db_column='orderId', max_length=40, blank=True, null=True)
    productcode = models.CharField(db_column='productCode', max_length=8, blank=True, null=True)
    customercode = models.IntegerField(db_column='customerCode', blank=True, null=True)
    requestindex = models.IntegerField(db_column='requestIndex', blank=True, null=True)
    referencenumber = models.CharField(db_column='referenceNumber', max_length=12, blank=True, null=True)
    notificationmessage = models.CharField(db_column='notification_message', max_length=200, blank=True, null=True)
    status = models.CharField(db_column='status', max_length=30, blank=True, null=True)
    documentlocation = models.CharField(db_column='documentLocation', max_length=200, blank=True, null=True)
    url = models.CharField(db_column='url', max_length=2000, blank=True, null=True)
    lastupdated = models.DateTimeField(db_column='last_updated', blank=True, null=True)
    requestornotified = models.SmallIntegerField(db_column='requestorNotified', blank=True, null=True)
    dataprocessed = models.SmallIntegerField(db_column='dataProcessed', blank=True, null=True)
    documentdelivered = models.SmallIntegerField(db_column='documentDelivered', blank=True, null=True)
    priority = models.IntegerField(db_column='priority')
    orderdatetime = models.DateTimeField(db_column='order_datetime', null=True)
    dateclosed = models.DateTimeField(db_column='date_closed', null=True)

    class Meta:
        managed = False
        db_table = 'lrs_search_transaction_tbl'

    def __str__(self):
        return f"Order ID: {self.orderid}"

    def get_order_id(self):
        order_id = self.orderid.replace("HAZPEXA","")
        return order_id






class LrsPayload(models.Model):
    orderId = models.CharField(db_column='orderId', max_length=30, primary_key=True)
    productcode = models.CharField(db_column='productCode', max_length=8, blank=True, null=True)
    lotNumber = models.CharField(db_column='lotNumber', max_length=9, blank=True, null=True)
    sectionNumber = models.CharField(db_column='sectionNumber', max_length=9, blank=True, null=True)
    planType = models.CharField(db_column='planType', max_length=4, blank=True, null=True)
    planNumber = models.CharField(db_column='planNumber', max_length=2, blank=True, null=True)
    ownersName = models.CharField(db_column='ownersName', max_length=50, blank=True, null=True)
    councilName = models.CharField(db_column='councilName', max_length=200, blank=True, null=True)
    consolidatedLot = models.SmallIntegerField(db_column='consolidatedLot', default=0)
    serviceLocationFlag = models.SmallIntegerField(db_column='serviceLocationFlag',default=0)
    propertyType = models.IntegerField(db_column='propertyType', blank=True, null=True)
    propertyAddressFlatNumber = models.CharField(db_column='propertyAddressFlatNumber', max_length=200, blank=True, null=True)
    propertyAddressFlatType = models.CharField(db_column='propertyAddressFlatType', max_length=200, blank=True, null=True)
    propertyAddressPostcode = models.CharField(db_column='propertyAddressPostcode', max_length=200, blank=True, null=True)
    propertyAddressState = models.CharField(db_column='propertyAddressState', max_length=200, blank=True, null=True)
    propertyAddressStreetName = models.CharField(db_column='propertyAddressStreetName', max_length=200, blank=True, null=True)
    propertyAddressStreetNumber = models.CharField(db_column='propertyAddressStreetNumber', max_length=200, blank=True, null=True)
    propertyAddressStreetType = models.CharField(db_column='propertyAddressStreetType', max_length=200, blank=True, null=True)
    propertyAddressSuburb = models.CharField(db_column='propertyAddressSuburb', max_length=200, blank=True, null=True)
    referenceNumber = models.CharField(db_column='referenceNumber', max_length=200, blank=True, null=True)
    folioIdentifier = models.CharField(db_column='folioIdentifier', max_length=200, blank=True, null=True)
    imageType = models.CharField(db_column='imageType', max_length=200, blank=True, null=True)
    imageReferenceNumber = models.CharField(db_column='imageReferenceNumber', max_length=200, blank=True, null=True)
    pageRange = models.CharField(db_column='pageRange', max_length=200, blank=True, null=True)
    subType = models.CharField(db_column='subType', max_length=5, blank=True, null=True)
    customerCode = models.IntegerField(db_column='customerCode', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lrs_payload_tbl'


class LrsProductPricing(models.Model):
    product_code = models.CharField(db_column="product_code", max_length=8, primary_key=True)
    product_description = models.CharField(db_column="product_description", max_length=100, null=False)
    product_price = models.FloatField(db_column="product_price", default=0)
    product_gst_fees = models.CharField(db_column="product_gst_fees", max_length=10, null=False)
    lrs_product_fees = models.FloatField(db_column="lrs_product_fees", default=0)
    lrs_product_gst_fees = models.CharField(db_column="lrs_product_gst_fees", max_length=10, null=False)
    total = models.FloatField(db_column="total", default=0)

    class Meta:
        managed = False
        db_table = "lrs_product_pricing"





def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_pdf_path(instance, filename):
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "Invoices/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)




class LrsInvoice(models.Model):
    invoice_id = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    company_code = models.CharField(max_length=100)
    searches_from = models.DateField(db_column='Searches_From', blank=True, null=True)  # Field name made lowercase.
    searches_to = models.DateField(db_column='Searches_To', blank=True, null=True)  # Field name made lowercase.
    searches_no = models.CharField(db_column='Searches_No', blank=True, null=True, max_length=100)  # Field name made lowercase.
    search_charge = models.FloatField(db_column='Search_Charge', blank=True, null=True)  # Field name made lowercase.
    service_charge = models.FloatField(db_column='Service_Charge', blank=True, null=True)  # Field name made lowercase.
    gst_charge = models.FloatField(db_column='GST_charge')  # Field name made lowercase.
    total_price = models.FloatField()
    pdf_link = models.FileField(upload_to=upload_pdf_path, null=True, blank=True)  # Field name made lowercase.
    payment_status = models.CharField(max_length=100)
    date_generated = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'lrs_invoice'





class Company(models.Model):
    companyindex = models.IntegerField(db_column='companyIndex', primary_key=True)  # Field name made lowercase.
    companyid = models.IntegerField(db_column='companyId')  # Field name made lowercase.
    compname = models.CharField(db_column='compName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    compcode = models.CharField(db_column='compCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    compstreet = models.CharField(db_column='compStreet', max_length=255, blank=True, null=True)  # Field name made lowercase.
    compsuburb = models.CharField(db_column='compSuburb', max_length=100, blank=True, null=True)  # Field name made lowercase.
    compstate = models.CharField(db_column='compState', max_length=50, blank=True, null=True)  # Field name made lowercase.
    comppostcode = models.CharField(db_column='compPostcode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    compphone1 = models.CharField(db_column='compPhone1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    mailstreet = models.CharField(db_column='mailStreet', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mailsuburb = models.CharField(db_column='mailSuburb', max_length=100, blank=True, null=True)  # Field name made lowercase.
    mailstate = models.CharField(db_column='mailState', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mailpostcode = models.CharField(db_column='mailPostcode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    directcontact = models.CharField(db_column='directContact', max_length=100, blank=True, null=True)  # Field name made lowercase.
    directcontactnumber = models.CharField(db_column='directContactNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    directcontactmobile = models.CharField(db_column='directContactMobile', max_length=30, blank=True, null=True)  # Field name made lowercase.
    directfaxnumber = models.CharField(db_column='directFaxNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='groupId', blank=True, null=True)  # Field name made lowercase.
    faxnumberareacode = models.CharField(db_column='faxNumberAreaCode', max_length=3, blank=True, null=True)  # Field name made lowercase.
    compfax1 = models.CharField(db_column='compFax1', max_length=10, blank=True, null=True)  # Field name made lowercase.
    compemail1 = models.CharField(db_column='compEmail1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    compdirectphonenumberareacode = models.CharField(db_column='compDirectPhoneNumberAreaCode', max_length=3, blank=True, null=True)  # Field name made lowercase.
    comphomephonenumberareacode = models.CharField(db_column='compHomePhoneNumberAreaCode', max_length=3, blank=True, null=True)  # Field name made lowercase.
    clientonline = models.IntegerField(blank=True, null=True)
    groupidmanual = models.IntegerField(db_column='groupIdManual', blank=True, null=True)  # Field name made lowercase.
    companyacn = models.CharField(db_column='CompanyACN', max_length=30, blank=True, null=True)  # Field name made lowercase.
    companyabn = models.CharField(db_column='CompanyABN', max_length=30, blank=True, null=True)  # Field name made lowercase.
    msrepl_tran_version = models.CharField(max_length=10, blank=True, null=True)
    markfordeletion = models.IntegerField(db_column='MarkForDeletion', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    directcontactareacode = models.CharField(db_column='directContactAreaCode', max_length=3, blank=True, null=True)  # Field name made lowercase.
    settlementclient = models.IntegerField(db_column='SettlementClient', blank=True, null=True)  # Field name made lowercase.
    # iquoteenabled = models.TextField(db_column='iQuoteEnabled', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    dxnumber = models.CharField(db_column='DXNumber', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dxexchange = models.CharField(db_column='DXExchange', max_length=20, blank=True, null=True)  # Field name made lowercase.
    billingmethod = models.IntegerField(db_column='BillingMethod', blank=True, null=True)  # Field name made lowercase.
    column1 = models.CharField(db_column='COLUMN1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    column2 = models.CharField(db_column='COLUMN2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    column3 = models.CharField(db_column='COLUMN3', max_length=100, blank=True, null=True)  # Field name made lowercase.
    column4 = models.CharField(db_column='COLUMN4', max_length=100, blank=True, null=True)  # Field name made lowercase.
    column5 = models.CharField(db_column='COLUMN5', max_length=100, blank=True, null=True)  # Field name made lowercase.
    column6 = models.CharField(db_column='COLUMN6', max_length=100, blank=True, null=True)  # Field name made lowercase.
    discount = models.ForeignKey('LrsDiscountTbl', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_external'



class InvoiceItems(models.Model):
    id = models.BigAutoField(primary_key=True)
    count = models.IntegerField(null=True)
    username = models.CharField(max_length=100, null=True)
    date_ordered = models.DateField(null=True)
    reference = models.CharField(max_length=100, null=True)
    client_reference = models.CharField(max_length=100, null=True)
    disb = models.FloatField(null=True)
    charge = models.FloatField(null=True)
    disb_charge = models.FloatField(null=True)
    gst_amount = models.FloatField(null=True)
    gst_inc = models.FloatField(null=True)
    include = models.BooleanField(default=True)
    transaction= models.IntegerField(null=True)
    invoice = models.ForeignKey(LrsInvoice, on_delete=models.CASCADE, null=True)
    date_closed = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'invoice_items'


class LrsInvoicePayment(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateTimeField(default=timezone.now)
    invoice = models.ForeignKey(LrsInvoice, on_delete=models.CASCADE,  db_column='invoice')

    class Meta:
        managed = False
        db_table = 'invoice_payment_details'


class LrsDiscountTbl(models.Model):
    discount = models.FloatField()
    product_code = models.CharField(max_length=10,blank=True, null=True)
    is_percent = models.BooleanField(default=False)
    is_total = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'discount_tbl'

    def getDiscountFor(self):
        if self.is_total:
            discount_for = "Total Invoice"
        else:
            discount_for = self.product_code

        return discount_for


    def getSign(self):
        if self.is_percent:
            sign = "%"
        else:
            sign = "$"

        return sign


class LrsBillingCode(models.Model):
    billing_code = models.CharField(db_column="billing_code", max_length=8, primary_key=True)
    product_price = models.FloatField(db_column="product_price", default=0)
    code_type = models.CharField(max_length=10, blank=True, null=True)
    product_code = models.ForeignKey(LrsProductPricing, on_delete=models.CASCADE, db_column='product_code',related_name="product_pricing")
    class Meta:
        managed = False
        db_table = "lrs_billing_code"


class LrsResponsePayload(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    orderId = models.ForeignKey(LrsPayload, to_field="orderId", db_column='orderId', on_delete=models.CASCADE,
                                 null=True, related_name="respo")
    response = models.TextField(null= True)
    statusCode = models.IntegerField(null=True)
    client_payload = models.TextField(null= True)
    data_process = models.IntegerField(default=0)
    order_datetime = models.DateField(null=True)
    hazlett_status = models.IntegerField(null=True)
    update_date = models.DateTimeField(null=True,blank=True)

    class Meta:
        managed = False
        db_table = "lrs_response_payload"

    def get_hazlett_status(self):
        if self.hazlett_status == 0:
            val = "Submitted to LRS"
        elif self.hazlett_status == 1:
            val = "Data Input Error"
        else :
            val = "System Unavailable"

        return val


# class LrsDocumentStatus(models.Model):
#     id = models.CharField(max_length=8, primary_key=True)
#     status = models.IntegerField(null=True)
#     api_response = models.TextField(null= True)
#     orderId = models.ForeignKey(LrsResponsePayload, to_field="orderId", db_column='orderId', on_delete=models.CASCADE)
#
#     class Meta:
#         managed = False
#         db_table = 'lrs_document_status'

class LrsSearchNotBilled(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    orderId = models.ForeignKey(LrsPayload, to_field="orderId", db_column='orderId', on_delete=models.CASCADE,
                                 null=True, related_name="documentstatus")
    response = models.TextField(null= True)
    statusCode = models.IntegerField(null=True)
    client_payload = models.TextField(null= True)
    order_datetime = models.DateField(null=True)

    class Meta:
        managed = False
        db_table = "lrs_searches_not_billed"



    def get_order_id(self):
        order_id = self.orderId.referenceNumber
        return order_id
