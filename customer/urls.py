from django.urls import path, re_path
from customer.views import *

app_name = "customer"
urlpatterns = [
    # re_path(r'^$', index),
    path('shop/', shop),
    path('detail/<id>/', detail, name="detail"),
    path('ucf/', user_center_info),
    path('uco/', user_center_order),
    path('ucs/', user_center_site),
    path('changeinfo/', changeinfo, name="changeinfo"),
    path('change_address/<id>/', change_address),
    path('setdefault/', setdefault),
    path('delete/', delete),
]
