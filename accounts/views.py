from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from loyaltypoints.models import userprofile
from .forms import RegisterForm,CustomerLoginForm
from django.views.generic import CreateView
#from points.models import customer
# Create your views here.

def Register(request):
    if request.method == "POST":
        name = request.POST["Name"]
        uname = request.POST["username"]
        mobile_ = request.POST['PhoneNo']
        pwd1 = request.POST['password']
        pwd2 = request.POST['Confirm Password']
        email = request.POST['Email']
        address_ = request.POST['address']
        city_ = request.POST['city']
        


        if pwd1 == pwd2:
            if User.objects.filter(username=uname).exists():
                messages.info(request,"Username Aready in Use")
                return redirect("http://127.0.0.1:8000/register")


            elif userprofile.objects.filter(mobile=mobile_).exists():
                messages.info(request,"Mobile No Aready in Use")
                return redirect("http://127.0.0.1:8000/register")

            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email ID Aready in Use")
                return redirect("http://127.0.0.1:8000/register")
            else:
                
                user1 = User.objects.create_user(username=uname,password=pwd1,email=email,first_name=name,)
                user1.save()
                if city_=='Bengaluru':
                    state_ = 'Karnataka'
                   
                elif city_=='Chennai':
                    state_ = 'Tamil Nadu'
                    
                elif city_=='Hyderabad':
                    state_ = 'Telgana'
                    
                custom = userprofile.objects.create(user=user1,mobile=mobile_,default_address=address_,city=city_,state=state_)
                custom.save()
                
                return render(request,"accounts/index.html")
        else:
            messages.info(request,"Both Password and Confirm password are not matching")
            return redirect("http://127.0.0.1:8000/register")

        
    else:
        return render(request,"accounts/new reg.html")

def logout(request):
    auth.logout(request)
    return redirect("http://127.0.0.1:8000/")


def login(request):
    if request.method == "POST":
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            pwd1 = form.cleaned_data.get('password')
        
            user = auth.authenticate(username=uname,password=pwd1)
            if user is not None:
                auth.login(request,user)
                return redirect('http://127.0.0.1:8000/')
            else:
                return render(request, 'accounts/login.html', {
                    'form': form,
                    'error_message': 'Invalid Credential'
                })
    else:
        form = CustomerLoginForm()
        return render(request, 'accounts/login.html',{'form':form}) 

def passwordsucess(request):
    return render(request,'accounts/passsucess.html')

def register_user(request):
    template = "accounts/formregister.html"
    if request.method == 'POST':
       form = RegisterForm(request.POST)
       if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            elif userprofile.objects.filter(mobile=form.cleaned_data['mobile']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Mobile no already exists.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })

            elif len(form.cleaned_data['Name'])<3:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Please Enter a Valid Name'
                })

            elif len(form.cleaned_data['username'])<3:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Please Enter a Valid User Name'
                })

         
            else:
                # Create the user:
                user1 = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user1.first_name = form.cleaned_data['Name']
                user1.save()
                city_ = form.cleaned_data['city']

                if city_=='Bengaluru':
                    state_ = 'Karnataka'
                
                elif city_=='Chennai':
                    state_ = 'Tamil Nadu'
                    
                elif city_=='Hyderabad':
                    state_ = 'Telangana'
                userp = userprofile.objects.create(user=user1,mobile=form.cleaned_data['mobile'],default_address=form.cleaned_data['default_address'],city=city_,state=state_)
                return render(request,"accounts/index.html") 

    else:
        form = RegisterForm()
    return render(request, template, {'form': form})