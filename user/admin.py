from django.contrib import admin
from .models import *
# Register your models here.

class CompanyAdmin(admin.ModelAdmin):
    search_fields = ('companyid','compname','compcode',)
admin.site.register(Company,CompanyAdmin)

class UserAdmin(admin.ModelAdmin):
    search_fields = ('username',)
admin.site.register(UserCustomer, UserAdmin)

class SearchMasterAdmin(admin.ModelAdmin):
    search_fields = ('haz_order_id', 'customer_code', 'order_datetime', 'internal_username',  'applicationid',)
admin.site.register(SwSearchMasterTbl, SearchMasterAdmin)

class CustomerMasterAdmin(admin.ModelAdmin):
    search_fields = ('customer_code', 'customer_name', 'customer_type', 'username',)
admin.site.register(HazCustomerMasterTbl, CustomerMasterAdmin)

class AuthAdmin(admin.ModelAdmin):
    search_fields = ('username', 'first_name', 'last_name', 'email',)
admin.site.register(AuthUser, AuthAdmin)

class AuthPermissionsAdmin(admin.ModelAdmin):
    search_fields = ('user',)
admin.site.register(AuthUserUserPermissions, AuthAdmin)

class SwInvoiceAdmin(admin.ModelAdmin):
    search_fields = ('invoice_id','id','company_name', 'searches_from', 'cmpany_code', 'payment_status',)
admin.site.register(SwInvoice, SwInvoiceAdmin)

admin.site.register(SwInvoiceExternal)
admin.site.register(InvoiceItems)
admin.site.register(CompanyExternal)