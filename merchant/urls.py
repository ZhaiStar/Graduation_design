from django.urls import path, re_path
from merchant.views import *

app_name = "merchant"

urlpatterns = [

    re_path('^$', list_goods, name="list_goods"),
    path('sales', sales_analysis, name="sales"),
    path('add_goods', add_goods, name="add_goods"),
    path('get_fenlei', get_fenlei, name="get_fenlei"),
    path('ordermanage', orderManage, name="ordermanage"),
    path('banner', bannerManage, name="banner"),
    path('sales_analysis', sales_analysis, name="analysis"),
    path('analysis_data', analysis_data, name="analysis_data"),
    re_path(r'delbanner/(?P<id>\d+)', delbanner, name="delbanner"),
    re_path(r'change/(?P<id>\d+)', change, name="change"),
    re_path(r'set_state/(?P<id>\d+)', set_state, name="set_state"),
    re_path(r'order_state/(?P<id>\d+)', order_state, name="order_state"),
]
