from loyaltypoints.models import *
from django.forms import ModelForm
from django import forms
from django.core import validators

CITY_CHOICES =( 
    ("",""),
    ("Bengaluru", "Bengaluru"), 
    ("Chennai", "Chennai"), 
    ("Hyderabad", "Hyderabad"),
)
class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'input--style-4'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'input--style-4','pattern':"[a-z0-9._%+-]+@[a-z0-9.-]+.[a-z]{2,4}",'title':"Please Enter Valid Email Id eg:V****@mail.com"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input--style-4','pattern':"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",'title':'Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input--style-4'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'input--style-4','pattern':'[A-Za-z ]+', 'title':'Enter Characters Only '}))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class':'input--style-4','pattern':'[6-9]{4}[0-9]{6}','title':"Please Enter Valid 10 Mobile Number"}))
    default_address = forms.CharField(widget=forms.TextInput(attrs={'class':'input--style-4'}))
    city = forms.ChoiceField(choices=CITY_CHOICES,required=True)

class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'input--style-4'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input--style-4'}))
 