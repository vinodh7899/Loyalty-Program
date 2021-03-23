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
    Name = forms.CharField(widget=forms.TextInput(attrs={'class':"input--style-4",'pattern':'[A-Za-z ]+', 'title':'Enter Characters Only '}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'input--style-4'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'input--style-4','pattern':"[a-z0-9._%+-]+@[a-z0-9.-]+.[a-z]{2,4}",'title':"Please Enter Valid Email Id eg:V****@mail.com"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input--style-4','pattern':"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",'title':'Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input--style-4'}))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class':'input--style-4','pattern':'[6-9]{4}[0-9]{6}','title':"Please Enter Valid 10 Mobile Number"}))
    default_address = forms.CharField(widget=forms.TextInput(attrs={'class':'input--style-4'}))
    city = forms.ChoiceField(choices=CITY_CHOICES,required=True)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['city'].widget.attrs['class'] = 'input--style-4'

    def clean(self):
      super(RegisterForm, self).clean()

      # getting username and password from cleaned_data
      Name = self.cleaned_data.get('Name')
      username = self.cleaned_data.get('username')
      password = self.cleaned_data.get('password')
      default_address = self.cleaned_data.get('default_address')


'''
      # validating the username and password
      if not Name:
          self._errors['Name'] = self.error_class(['Please Enter a Valid Name'])


      if not username:
          self._errors['Name'] = self.error_class(['Please Enter a Valid User Name oooo'])

      else: 
         len(username) < 3
         self._errors['username'] = self.error_class(['Please Enter a Valid User Name'])
      if not default_address:
          self._errors['default_address'] = self.error_class(['Please Enter a Valid Address'])

      else:
         len(default_address) < 3
         self._errors['default_address'] = self.error_class(['Please Enter a Valid Address'])  

      return self.cleaned_data
'''


class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'input--style-4'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input--style-4'}))
 