from django.urls import path,include
from .views import *
app_name = 'loyaltypoints'

urlpatterns =[
    path("",products,name='products'),
    path("add-to-cart/<slug>/",add_to_cart,name='add-to-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,name='remove-single-item-from-cart'),
    path("order-summary/",Checkout.as_view(), name='order-summary'),
    #path("order-summary1/",redeem, name='order-summary1'),
    #path("complete-order1/<slug>/",completeorder, name='complete-order1'),
    path("complete-order2/<slug>/",completeorder2, name='complete-order2'),
    path("ordersuces/<slug>/",referid, name='ordersuces'),
    #path("complete-order2/<slug>/",completeorder2, name='complete-order2'),
    path("customerprofile2/",customerprofile, name='customerprofile2'),
    path("editprofile/",edit, name='editprofile'),
    path("addresschange/<slug>/",addressedit, name='addresschange'),

    path("customerprofile2/order-<int:pk>/", CustomerOrderDetailView.as_view(),
         name="customerorderdetail"),





]