from django.contrib import admin
from .models import *
# Register your models here.
class ProductPricingAdmin(admin.ModelAdmin):
    search_fields = ('product_code',)

class DiscountAdmin(admin.ModelAdmin):
    search_fields = ('companies_code',)

class ProductAdmin(admin.ModelAdmin):
    search_fields = ('product_code',)

# class DiscountCompAdmin(admin.ModelAdmin):
#     search_fields = ('companies_code',)

admin.site.register(SwProductPricing, ProductPricingAdmin)
admin.site.register(DiscountTbl, DiscountAdmin)
admin.site.register(SwProductsTbl,ProductAdmin)
# admin.site.register(DiscountCompany, DiscountCompAdmin)