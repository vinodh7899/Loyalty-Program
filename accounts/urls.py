from django.urls import path,include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns =[
    path("register/",Register),
    path("register2/",register_user),
    path("login/",login),
    path("logout/",logout),
    path("passwordchanged/",passwordsucess),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='loyaltypoints/password.html',
            success_url = '/passwordchanged/'
        ),
        name='change_password'
    ),
]