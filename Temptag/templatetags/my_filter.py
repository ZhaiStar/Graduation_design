from django import template
from User.models import User, Cart, OrderInfo
from customer.models import Cloth

register = template.Library()


@register.filter
def get_name(obj):
    user = User.objects.get(account=obj)
    return user.name


@register.filter
def get_identity(obj):
    user = User.objects.get(account=obj)
    return user.identity


@register.filter
def get_sumcart(obj):
    cart = Cart.objects.filter(user_id=obj)
    return len(cart)


@register.filter
def get_cart(obj):
    cart = Cart.objects.filter(user_id=obj).order_by("-id")
    return cart[:3]


@register.filter
def vaild_title(obj):
    if len(obj) < 12:
        result = obj
    elif len(obj) < 24:
        result = obj[:10] + "<br>" + obj[10:]
    else:
        result = obj[:10] + "<br>" + obj[10:20] + "<br>" + obj[20:]
    return result

@register.filter
def vaild_name(obj):
    if len(obj) > 12:
        result = obj[:12]+"..."
    else:
        result = obj
    return result


@register.filter
def get_price(obj):
    return obj.split(",")[0] + " 优惠价:￥" + obj.split(",")[1] if "," in obj else obj


@register.filter
def phone(obj):
    return obj[:3] + "******" + obj[-3:]


@register.filter
def get_number(obj):
    order = OrderInfo.objects.filter(order_id=obj.id)
    number = 0
    for i in order:
        number += i.goods_number
    return number


@register.filter
def get_picture(obj):
    return obj.split(",")[0]


@register.filter
def add(obj):
    return int(obj) + 1


@register.filter
def sub(obj):
    return 1 if int(obj) - 1 == 0 else int(obj) - 1
