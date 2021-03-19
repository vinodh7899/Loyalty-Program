from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from loyaltypoints.models import userprofile
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
        uname = request.POST["Name"]
        pwd1 = request.POST['password']
        
        user = auth.authenticate(username=uname,password=pwd1)
        if user is not None:
            auth.login(request,user)
            return redirect('http://127.0.0.1:8000/')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('http://127.0.0.1:8000/login/')
    else:
        return render(request, 'accounts/login.html') 


def passw(request):
    use = userprofile.objects.get(user=request.user)
    if request.method == "POST":
        pwd1 = request.POST['password']
        newpwd1 = request.POST['newpassword']
        confirmpwd1 = request.POST['confirmpassword']
        if newpwd1 == confirmpwd1:
            name = use.user.first_name
            if User.objects.filter(password=pwd1,username=name).exists():
   
                u.set_password(newpwd1)
                u.save()
            print(" changed")
            return redirect("http://127.0.0.1:8000/")
        
        else:
            messages.info(request,"Entered Password is wrong")
            print("not changed")
            return redirect("http://127.0.0.1:8000/changepassword/")
   
    return render(request,'loyaltypoints/password.html',{'user':use})

def passwordsucess(request):
    return render(request,'accounts/passsucess.html')