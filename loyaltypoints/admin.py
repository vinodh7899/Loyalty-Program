from django.contrib import admin
from .views import *
from accounts.views import *
# Register your models here.
admin.site.register(orderitem)
admin.site.register(order)
admin.site.register(Item)
admin.site.register(order_details)
admin.site.register(userprofile)
admin.site.register(loyaltycoins)