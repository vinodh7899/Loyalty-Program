from django.shortcuts import render,get_object_or_404,redirect
from .models import Item,orderitem,order,order_details,userprofile,loyaltycoins,point_master
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView, DetailView, View,TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.db.models import Sum
import string
from .forms import editform
import random
from datetime import datetime
from django.http import HttpResponse

def create_ref_code(size=10, chars= string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def products(request):
    prod_list = Item.objects.all()
    return render(request,'loyaltypoints/index.html',{'produc':prod_list})

def customerprofile(request):
    details = loyaltycoins.objects.filter(user=request.user,points_exp__lt=datetime.now())
    for detai in details:
        detai.point_status=True
     
        detai.save()
    #coi = loyaltycoins.objects.filter(user=request.user,points_exp__lt=datetime.now()).update(point_status=True)
   
    total_earned=loyaltycoins.objects.filter(user=request.user,point_status=False).aggregate(Sum('points_earned')) 
    total_redeem1=loyaltycoins.objects.filter(user=request.user,point_status=False).aggregate(Sum('points_redeem')) 
    if not total_redeem1.get('points_redeem__sum'):
        total_redeem1['points_redeem__sum']=0
   
    details = userprofile.objects.get(user=request.user)
    if not total_earned.get('points_earned__sum'):
        total_earned['points_earned__sum']=0

  
    details.total_points=total_earned.get('points_earned__sum')-total_redeem1.get('points_redeem__sum')
    details.save()
    
    customer = userprofile.objects.get(user=request.user)
    orders = order.objects.filter(user=request.user).order_by("orderid")
    coina = loyaltycoins.objects.filter(user=request.user).order_by("point_id")
    context={'profile':customer,"ordereditems":zip(orders,coina),'loyal':coina,'total_redeem':total_redeem1.get('points_redeem__sum'),'total_earned':total_earned.get('points_earned__sum')}
    return render(request, "loyaltypoints/customerprofile.html",context)

   

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = orderitem.objects.get_or_create(
        item_details=item,
        user=request.user,
        ordered=False
    )
    order_qs = order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order1 = order_qs[0]
        # check if the order item is in the order
        if order1.products.filter(item_details__slug=item.slug).exists():
            order_item.quantity += 1
            
            order_item.save()
            
            messages.info(request, "This item quantity was updated.")
            return redirect("loyaltypoints:order-summary")
        else:

            order1.products.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("loyaltypoints:order-summary")
     
    else:      
        order1 = order.objects.create(
            user=request.user)
        order2 = order.objects.get(user=request.user,ordered=False)
        order2.products.add(order_item)
        messages.info(request, "This item was added to your cart.")

        return redirect("loyaltypoints:order-summary")

def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order1 = order_qs[0]
        # check if the order item is in the order
        if order1.products.filter(item_details__slug=item.slug).exists():
            order_item = orderitem.objects.filter(
                item_details=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order1.products.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("loyaltypoints:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("loyaltypoints:order-summary", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("loyaltypoints:order-summary", slug=slug)
    
class Checkout(View):
    def get(self, *args, **kwargs):
        try:
            order2 = order.objects.get(user=self.request.user, ordered=False)
            order2.total_price = order2.get_total()
            order2.save()
            coi = loyaltycoins.objects.filter(user=self.request.user,points_exp__lt=datetime.now()).update(point_status=True)
            total_pric=loyaltycoins.objects.filter(user=self.request.user,point_status=False).aggregate(Sum('points_earned')) 
            total_redeem1=loyaltycoins.objects.filter(user=self.request.user,point_status=False).aggregate(Sum('points_redeem')) 
            if total_pric.get('points_earned__sum'):
                details = userprofile.objects.get(user=self.request.user)
                details.total_points = total_pric.get('points_earned__sum')-total_redeem1.get('points_redeem__sum')
                details.save()
            userdetail = userprofile.objects.get(user=self.request.user)
            context = {
                'object': order2,
                'profile':userdetail  
            }
            return render(self.request, 'loyaltypoints/checkout.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")




def completeorder2(request,slug):
    objec = order.objects.get(user=request.user,orderid=slug)
    
    points_track = point_master.objects.get()
    userpro = userprofile.objects.get(user=request.user)
    context = {
        'order_obj':objec,
        'profile':userpro,
        'points_track':points_track
        
    }

    if request.method == 'POST':
            if userpro.total_points>=points_track.min_redeem:
                redeemp = request.POST['redeempoints']
                redeem = float(redeemp)
            else:
                redeem=0
            if order is not None:

                order_update = order.objects.get(user=request.user,ordered=False)
                order_update.ordered=True
                order_update.orderrefid=create_ref_code()
                order_update.orderid=slug
                order_update.save()
                order_item_update = orderitem.objects.filter(user=request.user,ordered=False)
                for item in order_item_update:
                    item.ordered = True
                    item.save()
                order2 = order.objects.get(user=request.user,orderid=slug)
                if userpro.total_points>=points_track.min_redeem:
                    total = order2.total_price-redeem
                else:
                    total = order2.total_price
                if total>points_track.from_point and total<points_track.to_point:
                    earned = total*points_track.percentage1

                    if userpro.total_points>=points_track.min_redeem:
                        coin = loyaltycoins.objects.create(user=request.user,points_earned=earned,points_redeem=redeem)
                                 
                    elif userpro.total_points<points_track.min_redeem:
                        coin = loyaltycoins.objects.create(user=request.user,points_earned=earned)
               
                elif total<points_track.from_point:
                    earned = points_track.min_points
                    if userpro.total_points>=points_track.min_redeem:
                        
                        coin = loyaltycoins.objects.create(user=request.user,points_earned=earned,points_redeem=redeem)
                    elif userpro.total_points<points_track.min_redeem:
                        coin = loyaltycoins.objects.create(user=request.user,points_earned=earned)
                        


                elif total>points_track.to_point:
                    
                    earned = total*points_track.percentage2
                    if earned>=points_track.max_points:
                        earned=points_track.max_points
                        if userpro.total_points>=points_track.min_redeem:
                            coin = loyaltycoins.objects.create(user=request.user,points_earned=earned,points_redeem=redeem)
                        elif userpro.total_points<points_track.min_redeem:
                            coin = loyaltycoins.objects.create(user=request.user,points_earned=earned)
                    else:
                        if userpro.total_points>=points_track.min_redeem:
                            coin = loyaltycoins.objects.create(user=request.user,points_earned=earned,points_redeem=redeem)
                                 
                        elif userpro.total_points<points_track.min_redeem:
                            coin = loyaltycoins.objects.create(user=request.user,points_earned=earned)


                
                
                coi = loyaltycoins.objects.filter(user=request.user,points_exp__lt=datetime.now()).update(point_status=True)
                total_earned=loyaltycoins.objects.filter(user=request.user,point_status=False).aggregate(Sum('points_earned')) 
                total_redeem1=loyaltycoins.objects.filter(user=request.user,point_status=False).aggregate(Sum('points_redeem')) 
                if not total_redeem1.get('points_redeem__sum'):
                    total_redeem1['points_redeem__sum']=0
   
                details = userprofile.objects.get(user=request.user)
                if not total_earned.get('points_earned__sum'):
                    total_earned['points_earned__sum']=0

  
                details.total_points=total_earned.get('points_earned__sum')-total_redeem1.get('points_redeem__sum')
                details.save()

                userp = userprofile.objects.get(user=request.user)
 

                totall = userp.total_points-redeem
                userp.total_points = totall
                userp.save()
                redeem_total = order2.total_price-redeem
                order2.total_price=redeem_total
                order2.save()
                final = loyaltycoins.objects.last()
                return redirect('loyaltypoints:ordersuces',slug=final.point_id)
            else:

                return redirect('loyaltypoints:order-summary')
    return render(request,'loyaltypoints/ordersummary.html',context)

def referid(request,slug):
    orde2 = order.objects.last()
    id1 = orde2.orderid
    order3 = order.objects.get(user=request.user,orderid=id1)
    coina = loyaltycoins.objects.get(user=request.user,point_id=slug)
    userpro = userprofile.objects.get(user=request.user)
    return render(request,'loyaltypoints/ordersuces.html',{'object':order3,'user':userpro,'point':coina})





class CustomerOrderDetailView(DetailView):
    template_name = "loyaltypoints/customerorderdetail.html"
    model = order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and userprofile.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            orders = order.objects.get(orderid=order_id)
            #if request.user.customer != order.cart.customer:
                #return redirect("ecomapp:customerprofile")
        else:
            return redirect("/login/")
        return super().dispatch(request, *args, **kwargs)



def editprofile(request):
    
    profile = userprofile.objects.get(user=request.user)
    if request.method=="POST":
        mobile_ = request.POST['mobile']
        defa_address = request.POST['address']
        if userprofile.objects.filter(mobile=mobile_).exists():
                messages.info(request,"Mobile No Aready in Use")
                return redirect("http://127.0.0.1:8000/editprofile")
        else:
            user_update = userprofile.objects.get(user=request.user)
            user_update.mobile=mobile_
            user_update.default_address=defa_address
            user_update.save()
            return redirect("http://127.0.0.1:8000/customerprofile2")
    context = {'profile':profile}
    return render(request,'loyaltypoints/edit_profile.html',context)
   
def edit(request):
    userp = userprofile.objects.get(user=request.user)
    form = editform(initial={'mobile': userp.mobile,'default_address':userp.default_address,"city":userp.city})
    
    if request.method == "POST":  
        form = editform(request.POST)
        if form.is_valid():  
            Mobile_ = form.cleaned_data.get("mobile")
            Address_ = form.cleaned_data.get("default_address")
            city_ = form.cleaned_data.get("city")

            if city_=='Bengaluru':
                state_ = 'Karnataka'
                   
            elif city_=='Chennai':
                state_ = 'Tamil Nadu'
                    
            elif city_=='Hyderabad':
                state_ = 'Telangana'
            user_update = userprofile.objects.get(user=request.user)
            user_update.mobile=Mobile_
            user_update.default_address=Address_
            user_update.city=city_
            user_update.state=state_
            user_update.save()
            return redirect("http://127.0.0.1:8000/customerprofile2")      
    context = {'form':form,'userp':userp} 
    return render(request,"loyaltypoints/edit_profile.html",context)

def addressedit(request,slug):
    userp = userprofile.objects.get(user=request.user)
    form = editform(initial={'mobile': userp.mobile,'default_address':userp.default_address,"city":userp.city})

    if request.method == "POST":  
        form = editform(request.POST) 
        if form.is_valid():  
            Mobile_ = form.cleaned_data.get("mobile")
            Address_ = form.cleaned_data.get("default_address")
            city_ = form.cleaned_data.get("city")

            if city_=='Bengaluru':
                state_ = 'Karnataka'
                   
            elif city_=='Chennai':
                state_ = 'Tamil Nadu'
                    
            elif city_=='Hyderabad':
                state_ = 'Telangana'
            user_update = userprofile.objects.get(user=request.user)
            user_update.mobile=Mobile_
            user_update.default_address=Address_
            user_update.city=city_
            user_update.state=state_
            user_update.save()
            return redirect("loyaltypoints:complete-order2", slug=slug)     
    context = {'form':form,'userp':userp} 
    return render(request,"loyaltypoints/changeaddress.html",context)





