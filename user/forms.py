from django.forms import ModelForm
from django import forms
from .models import *

class AddUserForm(ModelForm):
	account_name = forms.CharField(widget=forms.TextInput(
		attrs={
			'class':'form-control',
			'id':"userAccountName",
			'name':"userAccountName",
			'aria-describedby':"inputGroupPrepend"
		}
		))
	user_name = forms.CharField(widget=forms.TextInput(
		attrs={
			'class':'form-control',
			'id':"userUserName",
			'name':"userUserName",
			'aria-describedby':"inputGroupPrepend"
		}
		))
	password = forms.CharField(widget=forms.TextInput(
		attrs={
			'class':"form-control",
			'id':"userPassword",
			'name':"userPassword",
			'aria-describedby':"inputGroupPrepend",
		}
		))
	CHOICES = [('New','New'),('Existing','Existing')]
	order_status = forms.CharField(label="User Type",widget=forms.RadioSelect(
		choices=CHOICES)
	)
	class Meta:
		model=UserCustomer
		fields = '__all__'

