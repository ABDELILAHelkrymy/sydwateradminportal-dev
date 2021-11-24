from django.conf import settings
from django.db import models
from django.utils import timezone
import os
import random
from datetime import datetime
import pytz
# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_pdf_path(instance, filename):
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "Invoices/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)

class PropertyEnquiryFormTable(models.Model):
    SetIndex = models.IntegerField(null=False)
    SetId = models.IntegerField(primary_key=True)
    ClientId = models.IntegerField(null=True)
    ClientRef = models.CharField(max_length=50, null=True)
    Re = models.CharField(max_length=50, null=True)
    ClientOfficeRef = models.CharField(max_length=50, null=True)
    From = models.CharField(max_length=50, null=True)
    Post = models.CharField(max_length=50, null=True)
    DX = models.CharField(max_length=50, null=True)
    FromStreetAddress = models.CharField(max_length=100, null=True)
    Suburb = models.CharField(max_length=50, null=True)
    AppRef = models.CharField(max_length=50, null=True)
    CouncilName = models.CharField(max_length=50, null=True)
    Parish = models.CharField(max_length=50, null=True)
    County = models.CharField(max_length=50, null=True)
    Locality = models.CharField(max_length=50, null=True)
    HouseNumber = models.CharField(max_length=50, null=True)
    StreetName = models.CharField(max_length=50, null=True)
    NearXStreet = models.CharField(max_length=50, null=True)
    StreetSide = models.CharField(max_length=50, null=True)
    StreetDir = models.CharField(max_length=50, null=True)
    MapNo = models.CharField(max_length=50, null=True)
    GridRef = models.CharField(max_length=50, null=True)
    Frontage = models.CharField(max_length=50, null=True)
    Depth = models.CharField(max_length=50, null=True)
    Area = models.CharField(max_length=50, null=True)
    Nature = models.CharField(max_length=50, null=True)
    Lot = models.CharField(max_length=50, null=True)
    DP = models.CharField(max_length=50, null=True)
    SectionNumber = models.CharField(max_length=50, null=True)
    PrevPorNo = models.CharField(max_length=50, null=True)
    Por = models.CharField(max_length=50, null=True)
    PorSection = models.CharField(max_length=50, null=True)
    Allot = models.CharField(max_length=50, null=True)
    AllotSec = models.CharField(max_length=50, null=True)
    Town = models.CharField(max_length=50, null=True)
    SPLot = models.CharField(max_length=50, null=True)
    SP = models.CharField(max_length=50, null=True)
    SPLotNumber = models.CharField(max_length=50, null=True)
    SPDPNumber = models.CharField(max_length=50, null=True)
    FIVolFol = models.CharField(max_length=50, null=True)
    OSDeedBook = models.CharField(max_length=50, null=True)
    OSDeedNumber = models.CharField(max_length=50, null=True)
    OtherTypeLTORef = models.CharField(max_length=50, null=True)
    AssesValGenNumber = models.CharField(max_length=50, null=True)
    WaterBoardRef = models.CharField(max_length=50, null=True)
    OtherTypeCALMRef = models.CharField(max_length=50, null=True)
    SubName = models.CharField(max_length=50, null=True)
    SubStreetName = models.CharField(max_length=50, null=True)
    TownClerkEtc = models.CharField(max_length=50, null=True)
    SubLotNumber = models.CharField(max_length=50, null=True)
    SubPorNumber = models.CharField(max_length=50, null=True)
    SubDPNumber = models.CharField(max_length=50, null=True)
    SubSectionNumber = models.CharField(max_length=50, null=True)
    AreaDimension = models.CharField(max_length=50, null=True)
    RGNameAddress = models.CharField(max_length=100, null=True)
    OccName = models.CharField(max_length=50, null=True)
    VendorNameAddress = models.CharField(max_length=100, null=True)
    PurPrice = models.FloatField(null=True)
    PurNameAddress = models.CharField(max_length=100, null=True)
    PurOfEnq = models.CharField(max_length=50, null=True)
    ApplSig = models.CharField(max_length=50, null=True)
    ActFor = models.CharField(max_length=50, null=True)
    Date = models.DateTimeField(null=True)
    Ph = models.CharField(max_length=50, null=True)
    Fax = models.CharField(max_length=50, null=True)
    LastUpdated = models.DateTimeField(null=True)
    ServiceCharge = models.FloatField(null=True)
    ServiceCode = models.CharField(max_length=30, null=True)
    GSTServiceCharge = models.FloatField(null=True)
    msrepl_tran_version = models.CharField(max_length=150, null=False)
    AmountPaidOnSet = models.FloatField(null=True)
    SetActivatedDate = models.DateTimeField(null=True)
    bActivated = models.IntegerField(null=True)
    iQuoteId = models.IntegerField(null=True)
    Instructions = models.CharField(max_length=255, null=False)
    class Meta:
        managed = False
        db_table = 'PropertyEnquiryFormTable'

    def get_fee(self):
        return self.AmountPaidOnSet-(self.ServiceCharge + self.GSTServiceCharge)

class Document(models.Model):
    file_name = models.CharField(max_length=200,blank=True, null=True)
    file_date = models.DateTimeField(null=True)
    downloaded = models.BooleanField(default=False)
    downloaded_date = models.DateTimeField(null=True)
    processed = models.IntegerField(default=0)
    success = models.IntegerField(default=0)
    rejected = models.IntegerField(default=0)
    processed_date = models.DateTimeField(null=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'document'

    def get_downloaded(self):
        if self.downloaded:
            var = "Downloaded"
        else:
            var = "Inprogress"
        return var

    def get_processed(self):
        if self.downloaded:
            var = "File Processed"
        else:
            var = "In progress"
        return var

class Payload(models.Model):
    SearchID = models.CharField(max_length=220, null=True)
    ProductTitle = models.CharField(max_length=220, null=True)
    ProviderProductCode = models.CharField(max_length=220, null=True)
    LocalSearchDtls = models.CharField(max_length=220, null=True)
    OrderType = models.CharField(max_length=220, null=True)
    ReturnMethod = models.CharField(max_length=220, null=True)
    CouncilName = models.CharField(max_length=220, null=True)
    PropertyType = models.CharField(max_length=220, null=True)
    CreatedDate = models.CharField(max_length=220, null=True)
    FileNo = models.CharField(max_length=220, null=True)
    LotNo = models.CharField(max_length=220, null=True)
    PlanType = models.CharField(max_length=220, null=True)
    PlanNo = models.CharField(max_length=220, null=True)
    Area = models.CharField(max_length=220, null=True)
    TitleRef = models.CharField(max_length=220, null=True)
    PreviousDescr = models.CharField(max_length=220, null=True)
    StreetAddress = models.CharField(max_length=220, null=True)
    Suburb = models.CharField(max_length=220, null=True)
    Postcode = models.CharField(max_length=220, null=True)
    SettlementDate = models.CharField(max_length=220, null=True)
    BuyersName = models.CharField(max_length=220, null=True)
    BuyStreetAddress = models.CharField(max_length=220, null=True)
    BuySuburb = models.CharField(max_length=220, null=True)
    BuyState = models.CharField(max_length=220, null=True)
    BuyPostCode = models.CharField(max_length=220, null=True)
    SellersName = models.CharField(max_length=220, null=True)
    SellStreetAddress = models.CharField(max_length=220, null=True)
    SellSuburb = models.CharField(max_length=220, null=True)
    SellState = models.CharField(max_length=220, null=True)
    SellPostcode = models.CharField(max_length=220, null=True)
    PurchaseRail = models.CharField(max_length=220, null=True)
    CustomerID = models.CharField(max_length=220, null=True)
    FirstName = models.CharField(max_length=220, null=True)
    LastName = models.CharField(max_length=220, null=True)
    Workphone = models.CharField(max_length=220, null=True)
    FaxNumber = models.CharField(max_length=220, null=True)
    Email = models.CharField(max_length=220, null=True)
    CompanyName = models.CharField(max_length=220, null=True)
    PostalAddress = models.CharField(max_length=220, null=True)
    PostalCity = models.CharField(max_length=220, null=True)
    PostalState = models.CharField(max_length=220, null=True)
    PostalCode = models.CharField(max_length=220, null=True)
    file_id = models.CharField(max_length=220, null=True)
    file_name = models.CharField(max_length=220, null=True)
    processed = models.CharField(max_length=220, null=True)
    processed_date = models.CharField(max_length=220, null=True)
    created_date = models.CharField(max_length=220, null=True)
    completed_date = models.DateTimeField(null=True)
    error = models.CharField(max_length=220, null=True)
    propertyenquiryrequest_id = models.ForeignKey(PropertyEnquiryFormTable, on_delete=models.CASCADE,  db_column='propertyenquiryrequest_id', to_field='SetId',related_name="request_auth")
    class Meta:
        managed = False
        db_table = 'payload'

    def get_purchasers_name_address(self):
        if self.BuyStreetAddress:
            BuyStreetAddress = " , " + self.BuyStreetAddress
        else:
            BuyStreetAddres = ""
        if self.BuyState:
            BuyState = " , " + self.BuyState
        else:
            BuyState = ""
        self.purchasers_name_address = self.BuyersName + BuyStreetAddress + BuyState

    def get_prioprietors_name_address(self):
        if self.SellStreetAddress:
            SellStreetAddress = " , " + self.SellStreetAddress
        else:
            SellStreetAddress = ""
        if self.SellState:
            SellState = " , " + self.SellState
        else:
            SellState = ""
        return self.SellersName + SellStreetAddress + SellState

    def get_vendors_name_address(self):
        if self.StreetAddress:
            StreetAddress = " , " + self.StreetAddress
        else:
            StreetAddress = ""
        return self.FirstName + " " + self.LastName + StreetAddress

    def get_plan_type_dp(self):
        if self.PlanType.upper() == "DP":
            return "DP"
        else:
            return None

    def get_plan_type_sp(self):
        if self.PlanType.upper() == "SP":
            return "SP"
        else:
            return None

    def get_status(self):
        if self.processed == 0:
            return "None"
        elif self.processed == 1:
            return "In Progress"
        elif self.processed == 2:
            return "Rejected"
        elif self.processed == 3:
            return "Completed"
        elif self.processed == 4:
            return "Work In Progress"


class AuthCouncilPexaTable(models.Model):
    AuthNo = models.IntegerField(primary_key=True)
    RecordIndex = models.IntegerField(null=False,unique=True)
    Auth = models.CharField(max_length=50, null=True)
    AuthDX = models.CharField(max_length=50, null=True)
    AuthSuburb = models.CharField(max_length=50, null=True)
    AuthState = models.CharField(max_length=50, null=True)
    AuthPostCode = models.CharField(max_length=50, null=True)
    AuthPhoneNumber = models.CharField(max_length=50, null=True)
    EnquiryCost = models.FloatField(null=True)
    EnquiryGSTAmount = models.FloatField(null=True)
    EnquiryGSTReq = models.IntegerField(null=True)
    CostDrainageDiag = models.FloatField(null=True)
    Cost149 = models.FloatField(null=True)
    Cost1492 = models.FloatField(null=True)
    Cost1495 = models.FloatField(null=True)
    Cost603 = models.FloatField(null=True)
    CostNoxiousWeed = models.FloatField(null=True)
    CostWaterRates = models.FloatField(null=True)
    GSTCost603 = models.FloatField(null=True)
    GSTCost1492 = models.FloatField(null=True)
    GSTCost149 = models.FloatField(null=True)
    GSTCost1495 = models.FloatField(null=True)
    GSTCostDrainageDiag = models.FloatField(null=True)
    GSTCostNoxiousWeed = models.FloatField(null=True)
    GSTCostWaterRates = models.FloatField(null=True)
    GSTCostMisc = models.FloatField(null=True)
    GSTEnabledCost603 = models.IntegerField(null=True)
    GSTEnabledCost1492 = models.IntegerField(null=True)
    GSTEnabledCost1495 = models.IntegerField(null=True)
    GSTEnabledCost149 = models.IntegerField(null=True)
    GSTEnabledCostDrainageDiag = models.IntegerField(null=True)
    GSTEnabledCostNoxiousWeed = models.IntegerField(null=True)
    GSTEnabledCostWaterRates = models.IntegerField(null=True)
    GSTEnabledCostMisc = models.IntegerField(null=True)
    CouncilFlag = models.IntegerField(null=False)
    LastUpdated = models.DateTimeField(null=True)
    CostMisc = models.FloatField(null=True)
    AuthMiscellanous = models.IntegerField(null=True)
    msrepl_tran_version = models.CharField(max_length=20, null=False)
    RegionName = models.CharField(max_length=20, null=True)
    bDisabled = models.IntegerField(null=True)
    AuthDisplayOrder = models.IntegerField(null=True)
    EnergySource = models.CharField(max_length=20, null=True)
    ManualQuoteFlag = models.IntegerField(null=True)
    EnableUpdate = models.IntegerField(null=True)
    StatusUpdate = models.IntegerField(null=True)
    class Meta:
        managed = False
        db_table = 'AuthCouncilPexaTable'

    def __str__(self):
        return self.AuthNo





class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=200, null=False)

    class Meta:
        managed = False
        db_table = 'product'

class AuthRequestsTable(models.Model):
    AuthRequestIndex = models.IntegerField(primary_key=True)
    SetId = models.ForeignKey(PropertyEnquiryFormTable, on_delete=models.CASCADE,  db_column='SetId', to_field='SetId',related_name="request_setid")
    AuthNo = models.ForeignKey(AuthCouncilPexaTable, on_delete=models.CASCADE,  db_column='AuthNo', to_field='AuthNo',related_name="request_auth")
    Returned = models.IntegerField(null=True)
    CertTypeA = models.CharField(max_length=50, null=True)
    CertTypeB = models.CharField(max_length=50, null=True)
    CertTypeC = models.CharField(max_length=50, null=True)
    CertTypeD = models.CharField(max_length=50, null=True)
    Comments = models.CharField(max_length=50, null=True)
    DateReturned = models.DateTimeField(null=True)
    MiscAuth = models.CharField(max_length=50, null=True)
    MiscAuthDX = models.CharField(max_length=50, null=True)
    MiscAuthSuburb = models.CharField(max_length=50, null=True)
    MiscAuthPostCode = models.CharField(max_length=50, null=True)
    Online = models.IntegerField(null=False)
    Amount = models.FloatField(null=True)
    EnquiryGSTAmount = models.FloatField(null=True)
    EnquiryGSTReq = models.IntegerField(null=True)
    CreatedDate = models.DateTimeField(null=True)
    ServiceCode = models.ForeignKey(Product, on_delete=models.CASCADE,  db_column='ServiceCode', to_field='id',related_name="request_product")
    GSTIncCouncilPayment = models.IntegerField(null=True)
    msrepl_tran_version = models.CharField(max_length=150, null=False)
    class Meta:
        managed = False
        db_table = 'AuthRequestsTable'


class DocumentOutputTable(models.Model):
    id = models.BigAutoField(primary_key=True)
    client_ref = models.CharField(max_length=200, null=False)
    counter = models.IntegerField(null=True,default=0)

    class Meta:
        managed = False
        db_table = 'DocumentOutputTable'


class ServiceCharge(models.Model):
    id = models.IntegerField(primary_key=True)
    council_id = models.ForeignKey(AuthCouncilPexaTable, on_delete=models.CASCADE, related_name="service_council",  db_column='council_id')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="service_product",  db_column='product_id')
    council_fee = models.FloatField(default=0)
    hazlett_fee = models.FloatField(default=0)
    gst = models.FloatField(default=0)
    gst_enable =  models.IntegerField(default=0)
    total = models.FloatField(default=0)

    class Meta:
        managed = False
        db_table = 'service_charge'


class RatiesInvoice(models.Model):
    invoice_id = models.CharField(db_column='invoice_id',max_length=100)
    company_name = models.CharField(db_column='company_name',max_length=100)
    company_code = models.CharField(db_column='company_code',max_length=100)
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
        db_table = 'raties_invoice'

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
    request_id = models.ForeignKey(Payload,db_column='request_id',to_field='id',on_delete=models.CASCADE,related_name="invoice_item_search_transaction")
    invoice = models.ForeignKey(RatiesInvoice, on_delete=models.CASCADE, null=True)
    date_closed = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'invoice_items'

class RatiesInvoicePayment(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateTimeField(default=timezone.now)
    invoice = models.ForeignKey(RatiesInvoice, on_delete=models.CASCADE,  db_column='invoice')

    class Meta:
        managed = False
        db_table = 'invoice_payment_details'


class CommentTable(models.Model):
    payload = models.ForeignKey(Payload,db_column='payload',to_field='id',on_delete=models.CASCADE,related_name="comment_payload")
    comment = models.TextField(null=False)
    user = models.CharField(max_length=200, null=True,blank=True)
    created = models.DateTimeField(default=timezone.now)
    deleted = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'CommentTable'


    def get_utc_to_sydney(self):
        print("RATIES PY")
        if self.created == None:
            return None
        try:
            d1 = self.created
        except TypeError:
            raise
            pass

        d2 = d1.replace(tzinfo=pytz.UTC)
        d3 = d2.astimezone(pytz.timezone("Australia/Sydney"))

        return d3.strftime('%Y-%m-%d %I:%M %p')
