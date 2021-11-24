from django.db import models

class DiscountCompany(models.Model):
    company_code = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'discount_company'


class DiscountTbl(models.Model):
    discount = models.FloatField()
    companies_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discount_tbl'

class SwProductPricing(models.Model):
    product_code = models.CharField(primary_key=True, max_length=8)
    product_description = models.CharField(max_length=100)
    product_price = models.FloatField(blank=True, null=True)
    product_gst_fees = models.CharField(max_length=10)
    sw_product_fees = models.FloatField(blank=True, null=True)
    sw_product_gst_fees = models.CharField(max_length=10)
    total = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sw_product_pricing'


class SwProductsTbl(models.Model):
    product_code = models.CharField(primary_key=True, max_length=8)
    product_description = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'sw_products_tbl'



class ExternalDiscountTbl(models.Model):
    discount = models.FloatField()
    product_code = models.CharField(max_length=10,blank=True, null=True)
    is_percent = models.BooleanField(default=False)
    is_total = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'discount_external_tbl'

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


class SwProductPricingExternal(models.Model):
    product_code = models.CharField(primary_key=True, max_length=8)
    product_description = models.CharField(max_length=100)
    product_price = models.FloatField(blank=True, null=True)
    product_gst_fees = models.CharField(max_length=10)
    sw_product_fees = models.FloatField(blank=True, null=True)
    sw_product_gst_fees = models.CharField(max_length=10)
    total = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sw_product_pricing_external'