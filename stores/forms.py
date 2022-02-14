from django import forms
from django.forms import fields

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import *

PAYMENT_CHOICES = (
    ('Paypal','Paypal'),
    ('Paystack','Paystack')
)

class checkoutForm(forms.Form):
    street_address = forms.CharField( widget= forms.TextInput(attrs={'class':'form-control',
    'placeholder':'1234 Main St'}))
    apartment_address = forms.CharField(required=False,widget= forms.TextInput(attrs={'class':'form-control',
    'placeholder':'Apartment or suite'}))
    country = CountryField(blank_label = 'Select Country').formfield(widget= CountrySelectWidget(attrs={'class':'custom-select d-block w-100'}))
    zip = forms.CharField(widget= forms.TextInput(attrs={'class':'form-control'}))
    save_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)