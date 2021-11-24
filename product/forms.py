from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm
from .models import *

class PriceUpdateForm(BSModalModelForm):
	CHOICES = [('Yes','Yes'),('No','No')]
	product_price=forms.FloatField(widget=forms.TextInput(
	attrs={
		'class':'mb-2 form-control ',
	}
	),required = False)
	product_gst_fees=forms.CharField(widget=forms.RadioSelect(
        choices=CHOICES),required = False
    )
	sw_product_fees=forms.FloatField(widget=forms.TextInput(
	attrs={
		'class':'mb-2 form-control ',           
	}
	),required = False)
	sw_product_gst_fees=forms.CharField(widget=forms.RadioSelect(
        choices=CHOICES),required = False
    )
	class Meta:
		model = SwProductPricing
		exclude = ('user',)
		fields = ['product_price','product_gst_fees','sw_product_fees','sw_product_gst_fees']

class DiscountCreateForm(BSModalModelForm):
	discount=forms.FloatField(widget=forms.TextInput(
	attrs={
		'class':'mb-2 form-control',
		'placeholder':'Percentage %',           
	}
	),required = False)
	class Meta:
		model = DiscountTbl
		exclude = ('user',)
		fields = ['discount']



class ExternalDiscountCreateForm(BSModalModelForm):
	CHOICES = [('1', '%'), ('0', '$')]
	is_percent = forms.ChoiceField(choices=CHOICES, label="is_percent",
									 initial='', widget=forms.Select(attrs={
			'class': 'mb-2 form-control',
			'placeholder': 'Percentage %',
		}), required=True)

	product_code=forms.ChoiceField(choices=[], label="Discount for",
								  initial='', widget=forms.Select(	attrs={
		'class':'mb-2 form-control',
		'placeholder':'Percentage %',
	}), required=True)
	discount=forms.FloatField(widget=forms.TextInput(
	attrs={
		'class':'mb-2 form-control',
		'placeholder':'',
	}
	),required = False)

	def __init__(self, *args, **kwargs):
		super(ExternalDiscountCreateForm, self).__init__(*args, **kwargs)

		product_list = SwProductPricing.objects.all().values_list('product_code', flat=True)
		discount = ExternalDiscountTbl.objects.all()
		discount_total = discount.filter(is_total=1).count()
		discount_list = discount.values_list('product_code', flat=True)
		product_list
		new_list = []
		new_list.append(["", ""])
		for product_list_ in product_list:
			if not product_list_ in discount_list:
				new_list.append([product_list_, product_list_])
		if not discount_total:
			new_list.append(["1", "Total Invoice"])
		final_product_list = tuple(new_list)
		self.fields['product_code'].choices = final_product_list


	class Meta:
		model = ExternalDiscountTbl
		exclude = ('user',)
		fields = ['discount','product_code','is_percent']


class externalDiscountEditForm(BSModalModelForm):
	product_code=forms.CharField(widget=forms.TextInput(
	attrs={
		'class':'mb-2 form-control',
		'placeholder':'Percentage %',
		'readonly' : True,
	}
	),required = False)
	CHOICES = [('1', '%'), ('0', '$')]
	is_percent = forms.ChoiceField(choices=CHOICES, label="is_percent",
									 initial='', widget=forms.Select(attrs={
			'class': 'mb-2 form-control',
			'placeholder': 'Percentage %',
		}), required=True)
	discount=forms.FloatField(widget=forms.TextInput(attrs={'class':'mb-2 form-control','placeholder':'Percentage %',}),required = True)



	class Meta:
		model = ExternalDiscountTbl
		exclude = ('user',)
		fields = ['discount','product_code','is_percent']