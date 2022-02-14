from dataclasses import field, fields
from pyexpat import model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, widgets
from django.contrib.auth.models import User
from django import forms

from users.models import Profile

class Createuser(UserCreationForm):
    password1 = forms.CharField(
        label=("Password"),
        widget = forms.PasswordInput(attrs={'class':'form-control'}),
    )
    password2 = forms.CharField(
        label=("Confirm Password"),
        widget = forms.PasswordInput(attrs={'class':'form-control'}),
    )
    class Meta:
        model= User
        fields=['first_name','username','email','password1','password2']
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }

class Editprofile(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','username','profile_pix','email']
