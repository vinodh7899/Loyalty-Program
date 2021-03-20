from django.shortcuts import render,get_object_or_404,redirect
from .models import Item,orderitem,order,order_details,userprofile,loyaltycoins
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView, DetailView, View,TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.db.models import Sum
import string
import random
from datetime import datetime

def create_ref_code(size=10, chars= string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def products(request):
    prod_list = Item.objects.all()
    return render(request,'loyaltypoints/index.html',{'produc':prod_list})

def customerprofile(request):
    coi = loyaltycoins.objects.filter(user=request.user,points_exp__lt=datetime.now()).update(point_status=True)
    total_pric=loyaltycoins.objects.filter(user=request.user,point_status=False).aggregate(Sum('points_earned')) 
    total_redeem1=loyaltycoins.objects.filter(user=request.user,point_status=False).aggregate(Sum('points_redeem')) 
    details = userprofile.objects.get(user=request.user)
    if total_pric.get('points_earned__sum'):
            details.total_points = total_pric.get('points_earned__sum')-total_redeem1.get('points_redeem__sum')
            details.save()
    customer = userprofile.objects.get(user=request.user)
    orders = order.objects.filter(user=request.user).order_by("orderid")
    coina = loyaltycoins.objects.filter(user=request.user).order_by("point_id")
    context={'profile':customer,"ordereditems":orders,'loyal':coina}
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
    
    
    userpro = userprofile.objects.get(user=request.user)
    context = {
        'order_obj':objec,
        'profile':userpro
        
    }

    if request.method == 'POST':
            if userpro.total_points>=500:
                redeemp = request.POST['redeempoints']
                redeem = float(redeemp)
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
                if userpro.total_points>=500:
                    total = order2.total_price-redeem
                else:
                    total = order2.total_price
                if total>500 and total<2000:
                    earned = total*0.02
                    if earned<=100:
                        
                        if userpro.total_points>=500:
                            coin = loyaltycoins.objects.create(user=request.user,points_earned=earned,points_redeem=redeem)
                        elif userpro.total_points<500:
                            coin = loyaltycoins.objects.create(user=request.user,points_earned=earned)
               
                elif total<500:
                    earned = 0
                    if userpro.total_points>=500:
                        
                        coin = loyaltycoins.objects.create(user=request.user,points_earned=earned,points_redeem=redeem)
                    elif userpro.total_points<500:
                        coin = loyaltycoins.objects.create(user=request.user,points_earned=earned)


                elif total>2000:
                    
                    earned = total*0.05
                    if earned>=100:
                        earned=100
                        if userpro.total_points>=500:
                            coin = loyaltycoins.objects.create(user=request.user,points_earned=earned,points_redeem=redeem)
                        elif userpro.total_points<500:
                            coin = loyaltycoins.objects.create(user=request.user,points_earned=earned)
                coi = loyaltycoins.objects.filter(user=request.user,points_exp__lt=datetime.now()).update(point_status=True)
                total_pric=loyaltycoins.objects.filter(user=request.user,point_status=False).aggregate(Sum('points_earned')) 
                total_redeem1=loyaltycoins.objects.filter(user=request.user,point_status=False).aggregate(Sum('points_redeem')) 
                details = userprofile.objects.get(user=request.user)
                details.total_points = total_pric.get('points_earned__sum')-total_redeem1.get('points_redeem__sum')
                details.save()

                userp = userprofile.objects.get(user=request.user)
                
                if userp.total_points>=500  :
                    tota = userp.total_points-redeem
                    userp.total_points = tota
                    userp.save()
                    redtota = order2.total_price-redeem
                    order2.total_price=redtota
                    order2.save()  
                return redirect('loyaltypoints:ordersuces',slug=slug)
            else:

                return redirect('loyaltypoints:order-summary')
    return render(request,'loyaltypoints/ordersummary.html',context)

def referid(request,slug):
    order3 = order.objects.get(user=request.user,orderid=slug)
    coina = loyaltycoins.objects.filter(user=request.user).order_by("point_id")
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


   