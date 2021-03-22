from .models import *
from django.forms import ModelForm
from django import forms

CITY_CHOICES =( 
    ('c',"Choose Your City"),
    ("Bengaluru", "Bengaluru"), 
    ("Chennai", "Chennai"), 
    ("Hyderabad", "Hyderabad"),
)


class editform(forms.Form):
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class':'input--style-4','pattern':'[6-9]{4}[0-9]{6}','title':"Please Enter Valid 10 Mobile Number"}))
    default_address = forms.CharField(widget=forms.TextInput(attrs={'class':'input--style-4'}))
    city = forms.ChoiceField(choices=CITY_CHOICES,required=True)
