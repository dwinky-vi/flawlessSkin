from .models import Order, Product
from django import forms

class OrderForm(forms.ModelForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={
		"class": "input_data", "type": "text", "placeholder": " ",
	}), required=True)  # required значит что поле должно быть обязательно заполнено
	last_name = forms.CharField(widget=forms.TextInput(attrs={
		"class": "input_data", "type": "text", "placeholder": " ",
	}), required=False)
	phone = forms.CharField(widget=forms.TextInput(attrs={
		"class": "input_data", "type": "tel", "placeholder": " ",
	}), required=False)
	email = forms.CharField(widget=forms.EmailInput(attrs={
		"class": "input_data", "type": "email", "placeholder": " ",
	}))
	address = forms.CharField(widget=forms.TextInput(attrs={
		"class": "input_data", "type": "text", "placeholder": " ", "id": "address",
	}), required=False)
	
	class Meta:
		model = Order
		fields = ('first_name', 'last_name', 'phone', 'email', 'address')
