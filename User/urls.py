from django.urls import path, re_path
from User.views import *

app_name = "user"

urlpatterns = [
    path('register/', register, name="register"),
    path('logout/', logout,name="logout"),
    path('forget_pwd/', forget_pwd, name="forget_pwd"),
    path('reset_pwd/<email>/', password_reset),
    path('cart/', cart),
    path('addcart/', addCart, name="addcart"),
    path('delcart/', delCart, name="delcart"),
    path('place_order/', place_order, name="place_order"),
    path('delorder/', delorder, name="delorder"),
    path('pay/', get_pay, name="pay"),
    path('pay_result/', pay_result, name="pay_result"),
]
