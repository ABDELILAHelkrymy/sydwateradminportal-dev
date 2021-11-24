from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm
from django.views.generic import *
from .models import *


class ServiceChargesCreateForm(forms.Form):
        council_id= forms.ChoiceField(choices=[], required=True,widget=forms.Select(attrs={'class':'mb-2 form-control','placeholder':'',}))
        product_id= forms.ChoiceField(choices=[], required=True,widget=forms.Select(attrs={'class':'mb-2 form-control','placeholder':'',}))
        council_fee =forms.FloatField(widget=forms.NumberInput(attrs={'class':'mb-2 form-control','placeholder':'0.00','onfocusout':'myFunction()'}),required = True)
        hazlett_fee =forms.FloatField(widget=forms.NumberInput(attrs={'class':'mb-2 form-control','placeholder':'0.00','onfocusout':'myFunction()'}),required = False)
        gst =forms.FloatField(widget=forms.NumberInput(attrs={'class':'mb-2 form-control','placeholder':'0.00','onfocusout':'myFunction()'}),required = False)
        gst_enable =forms.BooleanField(required = False,widget=forms.CheckboxInput(attrs={'onclick':'myFunction()'}))
        total = forms.FloatField(widget=forms.NumberInput(attrs={'class':'mb-2 form-control','placeholder':'0.00',}),required = False)

        def __init__(self, *args, **kwargs):
            self.council_id = kwargs.pop('council_id', None)
            self.product_id = kwargs.pop('product_id', None)
            super(ServiceChargesCreateForm, self).__init__(*args, **kwargs)
            self.fields['council_id'].choices = self.council_id
            self.fields['product_id'].choices = self.product_id



class CustomBooleanField(models.BooleanField):

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return int(value) # return 0/1

class AuthCouncilCreateForm(forms.Form):
    Auth = forms.CharField(widget=forms.TextInput(attrs={ 'placeholder': '', }),required=True)
    AuthDx = forms.CharField(widget=forms.TextInput(attrs={ 'placeholder': '', }),required=False)
    AuthSuburb = forms.CharField(widget=forms.TextInput(attrs={ 'placeholder': '', }), required=True)
    AuthPostCode = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', }),required=False)
    AuthPhoneNumber = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', }),required=False)

    Cost149 = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '$0.00', }),required=False)
    Cost1492 = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '$0.00', }), required=False)
    Cost1495 = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '$0.00', }), required=False)
    Cost603 = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '$0.00', }), required=False)
    CostNoxiousWeed = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '$0.00', }), required=False)
    CostWaterRates = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '$0.00', }), required=False)
    CostDrainageDiag = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '$0.00', }), required=False)
    CostMisc = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '$0.00', }), required=False)

    GSTCost149 = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '$0.00', }),required=False)
    GSTCost1492 = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '$0.00', }), required=False)
    GSTCost1495 = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '$0.00', }), required=False)
    GSTCost603 = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '$0.00', }), required=False)
    GSTCostNoxiousWeed = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '$0.00', }), required=False)
    GSTCostWaterRates = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '$0.00', }), required=False)
    GSTCostDrainageDiag = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '$0.00', }), required=False)
    GSTCostMisc = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '$0.00', }), required=False)

    GSTEnabledCost149 = forms.BooleanField(required=False)
    GSTEnabledCost1492 = forms.BooleanField(required=False)
    GSTEnabledCost1495 = forms.BooleanField(required=False)
    GSTEnabledCost603 = forms.BooleanField(required=False)
    GSTEnabledCostNoxiousWeed = forms.BooleanField(required=False)
    GSTEnabledCostWaterRates = forms.BooleanField(required=False)
    GSTEnabledCostDrainageDiag = forms.BooleanField(required=False)
    GSTEnabledCostMisc = forms.BooleanField(required=False)


class AuthorityCreateForm(forms.Form):
    Auth = forms.CharField(widget=forms.TextInput(attrs={ 'placeholder': '', }),required=True)
    AuthDx = forms.CharField(widget=forms.TextInput(attrs={ 'placeholder': '', }),required=False)
    AuthSuburb = forms.CharField(widget=forms.TextInput(attrs={ 'placeholder': '', }), required=True)
    AuthPostCode = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', }),required=False)
    AuthPhoneNumber = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '', }),required=False)
    AuthMiscellanous = forms.BooleanField(required=False)
    EnquiryCost = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '$0.00', }),required=False)
    EnquiryGSTAmount = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': '$0.00', }), required=False)
    EnquiryGSTReq = forms.BooleanField(required=False)


class ProductCreateForm(forms.Form):
    product_name = forms.CharField(widget=forms.TextInput(attrs={ 'placeholder': '', }),required=True)


class DocumentFileUploadForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=True)


payload_status = (
    #(0, "None"),
    #(1, "In Progress"),
    #(2, "Rejected"),
    ("", "----"),
    (4, "Work In Progress"),
    (3, "Completed"),
)
class PayloadStatusForm(forms.Form):
    status = forms.ChoiceField(choices=payload_status, required=True,
                                   widget=forms.Select(attrs={'class': 'mb-2 form-control', 'placeholder': '', }))


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'mb-2 form-control',  'placeholder': '',"rows":5 }),required=False)
