from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.conf import settings
import random
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import F
from datetime import datetime,timedelta 

CATEGORY_CHOICES = (
    ('N','Nuts'),
    ('O','Oils'),
    ('P','Pasta'),
)


CITY_CHOICES = (
    ('Bengaluru','Bengaluru'),
    ('Chennai','Chennai'),
    ('Hyderabad','Hyderabad'),
)

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    img = models.ImageField(upload_to="pics")
    discount_price = models.FloatField()
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=1)
    slug = models.SlugField()

    def get_add_to_cart_url(self):
        return reverse("loyaltypoints:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("loyaltypoints:remove-single-item-from-cart", kwargs={
            'slug': self.slug
        })

    def __str__(self):
        return "{} and {}".format(self.name,self.category)


class orderitem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item_details = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    

    def get_total_item_price(self):
        return self.quantity * self.item_details.price

    def create_ref_code():
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

    


class order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    orderid = models.IntegerField(primary_key=True)
    products = models.ManyToManyField(orderitem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)
    orderrefid = models.CharField(max_length=20, blank=True, null=True)

    def get_total(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_total_item_price()
        return total

    def pointsearn1(self):
        pointsearn = 0
        if self.total_price>500 and self.total_price<2000:
            pointsearn=self.total_price*0.02
        elif self.total_price>2000:
            earn = self.total_price*0.05
            if earn>100:
                pointsearn=100
            else:
                pointsearn=earn
        return int(pointsearn)

    def get_orderid1(self):
        return reverse("loyaltypoints:complete-order1", kwargs={
            'slug': self.orderid
        })

    def get_order_sucess(self):
        return reverse("loyaltypoints:ordersuces", kwargs={
            'slug': self.orderid
        })
    
    def get_orderid2(self):
        return reverse("loyaltypoints:complete-order2", kwargs={
            'slug': self.orderid
        })
    def get_address(self):
        return reverse("loyaltypoints:addresschange", kwargs={
            'slug': self.orderid
        })


        

class order_details(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=50)
    mobileno = models.IntegerField()
    address = models.TextField(max_length=300,blank=True, null=True)
    city = models.CharField(max_length=50)
    

    def __str__(self):
        return "{} {}".format(self.user,self.mobileno)

class userprofile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=12,blank=True)
    default_address = models.CharField(max_length=500)
    city = models.CharField(choices=CITY_CHOICES,max_length=10)
    state = models.CharField(max_length=500,null=True,blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)
    total_points = models.IntegerField(default=0)

    def datepublished(self):
        return self.joined_on.strftime('%B %d %Y')



    def totalredeem(self):
        if self.total_points>=500:
            return self


def get_deadline():
    return datetime.today() + timedelta(days=365)

    
class loyaltycoins(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    points_earned = models.IntegerField()
    points_redeem = models.IntegerField(default=0)
    points_exp = models.DateTimeField(default=get_deadline)
    point_status = models.BooleanField(default=False)
    point_id = models.IntegerField(primary_key=True)
    order_info = models.ManyToManyField(order)

    def loyalid(self):
        return reverse("loyaltypoints:ordersuces", kwargs={
            'slug': self.point_id
        })

        
class point_master(models.Model):
    from_point = models.IntegerField()
    to_point = models.IntegerField()
    percentage1 = models.FloatField()
    percentage2 = models.FloatField()
    max_points = models.IntegerField()
    min_points = models.IntegerField()
    min_redeem = models.IntegerField()
    point_conversion = models.IntegerField()

