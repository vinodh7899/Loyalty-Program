from django.urls import path,include
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'accounts'


urlpatterns =[
    path("register2/",register_user,name='register2'),
    path("login/",login,name='login'),
    path("logout/",logout,name='logout'),
    path("passwordchanged/",passwordsucess),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='loyaltypoints/password.html',
            success_url = '/logout/'
        ),
        name='change_password'
    ),
]