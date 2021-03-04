import hashlib
import time

from django.http import JsonResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from User.pay import Pay
from User.sendEmail import sendMail
from django.shortcuts import render, redirect, reverse
# Create your views here.
from User.models import User, Cart, PayOrder, OrderInfo, UserAddress
from customer.models import Cloth
from django.contrib.auth.decorators import login_required

from merchant.models import Banner


def set_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


def valid_user(account):
    """
    如果username存在，返回数据
    =
    """
    try:
        user = User.objects.get(account=account)
    except Exception:
        return False
    else:
        return user


def valid_email(email):
    """
    如果username存在，返回数据
    =
    """
    try:
        user = User.objects.get(email=email)
    except Exception:
        return False
    else:
        return True


def valid_login(fun):
    def inner(request, *args, **kwargs):
        next = request.GET.get("referer", None)
        re = "/" + str(request.META.get("HTTP_REFERER")).split("/", 3)[-1]
        cookie_user = request.COOKIES.get("account")
        session_user = request.session.get("account")
        if cookie_user and session_user and cookie_user == session_user:
            return fun(request, *args, **kwargs)
        else:
            if next:
                login_url = "/login/?next=%s" % next
                # print(next)
            else:
                referer = "/" + str(request.META.get("HTTP_REFERER")).split("/", 3)[-1]
                login_url = "/login/?next=%s" % referer
                # print(referer)
            return redirect(login_url)
    return inner


def valid_cookie(fun):
    def inner(request, *args, **kwargs):
        cookie_user = request.COOKIES.get("account")
        if cookie_user:
            return fun(request, *args, **kwargs)
        else:
            login_url = "/login"
            return redirect(login_url)

    return inner


# 账号注册
def register(request):
    msg = ""
    if request.method == "POST":
        username = request.POST.get("user_name")
        account = request.POST.get("account")
        password = request.POST.get("pwd")
        pwd = request.POST.get("cpwd")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        if username != "" and account != "" and password != "" and email != "":
            if valid_user(account):
                msg = "该账号已被注册！"
            else:
                if 6 <= len(password) <= 8:
                    if pwd == password:
                        user = User()
                        user.name = username
                        user.account = account
                        user.password = set_password(password)
                        user.phone = phone
                        user.email = email
                        address = UserAddress()
                        address.receiver = user.name
                        address.phone = user.phone
                        address.user = user
                        user.save()
                        address.save()
                        return redirect("/login/")
                    else:
                        msg = "两次输入的密码不一致"
                else:
                    msg = "密码长度要在6-8位之间"
        else:
            msg = "用户名、账号、邮箱、密码不能为空"
    return render(request, "customer/register.html", locals())


# 退出
def logout(request):
    response = redirect("/")
    response.delete_cookie("account")
    response.delete_cookie("user_id")
    request.session.clear()
    return response


@csrf_exempt
@valid_login
def cart(request):
    account = request.COOKIES.get("account")
    user = User.objects.get(account=account)
    carts = Cart.objects.filter(user_id=user.id)
    banners = Banner.objects.filter(state=1)
    if request.method == "POST":
        data = request.POST
        order = PayOrder()
        order.order_number = str(time.time()).replace(".", "")
        total = 0
        ids = []
        for i in data:
            if "checked" in i:
                cart_id = data[i]
                ids.append(int(cart_id))
                cart = Cart.objects.get(id=int(cart_id))
                total += cart.total
        order.order_total = float(total)
        order.order_user = user
        address = UserAddress.objects.filter(user=user, state=1).first()
        if not address:
            address = UserAddress.objects.all().first()
        order.order_address = address.address

        for i in ids:
            cart = Cart.objects.get(id=i)
            order_info = OrderInfo()
            order_info.goods_name = cart.name
            order_info.goods_number = cart.number
            order_info.goods_price = cart.price
            order_info.goods_total = cart.total
            order_info.goods_picture = cart.picture
            order_info.order_id = order
            order_info.goods_color = cart.color
            order_info.goods_size = cart.size
            order_info.cart_id = cart.id
            order_info.cloth_id = cart.cloth_id
            order.save()
            order_info.save()
        return redirect(f"/user/place_order/?order_id={order.id}")
    return render(request, "customer/cart.html", locals())


# 忘记密码
def forget_pwd(request):
    msg1 = ""
    msg2 = ""
    if request.method == "POST":
        email = request.POST.get("email")
        if valid_email(email):
            code = sendMail(email)
            request.session["code"] = code
            request.session["email"] = email
            msg2 = "邮件已发生，请注意查收"
            return redirect(f"/user/reset_pwd/{email}")
        else:
            msg1 = "该邮箱没有绑定账号"
    return render(request, "customer/forgot-pwd.html", locals())


# 重置密码
def password_reset(request, email):
    msg = ""
    if request.method == "POST":
        pwd = request.POST.get("new_pwd")
        cpwd = request.POST.get("cpwd")
        code = request.POST.get("code")
        s_code = request.session.get("code")
        print(s_code)
        if pwd != cpwd:
            msg = "两次输入的密码不一致！"
        elif int(code) != int(s_code):
            msg = "验证码错误"
        else:
            user = User.objects.get(email=email)
            user.password = set_password(pwd)
            user.save()
            msg1 = "密码重置成功"
            return redirect("/login/")
    return render(request, "customer/reset_pwd.html", locals())


def addCart(request):
    result = {"state": "error", "data": ""}
    if request.method == "POST":
        user = request.COOKIES.get("user_id")
        cloth_id = request.POST.get("cloth_id")
        color = request.POST.get("color")
        size = request.POST.get("size")
        number = request.POST.get("number")
        total = request.POST.get("total")
        try:
            cloth = Cloth.objects.get(id=cloth_id)
        except Exception as e:
            result["data"] = str(e)
        else:
            cart = Cart()
            cart.user_id = user
            cart.name = cloth.title
            cart.price = cloth.discount_price if cloth.discount_price else cloth.price
            cart.color = color
            cart.size = size
            cart.number = number
            cart.total = total
            cart.picture = cloth.picture.split(",")[0]
            cart.cloth_id = cloth_id
            cart.save()
            result["state"] = "success"
            result["data"] = "加入购物车成功"
    return JsonResponse(result)


def delCart(request):
    result = {"state": "error", "data": ""}
    if request.method == "POST":
        cart_id = request.POST.get("cart_id")
        cart = Cart.objects.get(id=cart_id)
        cart.delete()
        result["state"] = "success"
        result["data"] = "删除成功"
    return JsonResponse(result)


@valid_login
def place_order(request):
    account = request.COOKIES.get("account")
    user = valid_user(account)
    address_list = UserAddress.objects.filter(user=user)
    order_id = request.GET.get("order_id")
    order = PayOrder.objects.filter(id=int(order_id)).first()
    order_info = order.orderinfo_set.all()
    return render(request, "customer/place_order.html", locals())


def delorder(request):
    result = {"state": "error", "data": ""}
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        order = PayOrder.objects.get(id=int(order_id))
        order.delete()
        result["state"] = "success"
        result["data"] = "删除成功"
    return JsonResponse(result)


@valid_login
def get_pay(request):
    order_id = request.GET.get("order_id")
    address_id = request.GET.get("address")
    address = UserAddress.objects.get(id=int(address_id))
    order = PayOrder.objects.get(id=int(order_id))
    order.order_address = address.address
    order.save()
    url = Pay(order.order_number, order.order_total, order.id)
    return redirect(url)


def pay_result(request):
    order_id = request.GET.get("order_id")
    order = PayOrder.objects.get(id=int(order_id))
    order.order_state = 1
    order.save()
    for o_i in order.orderinfo_set.all():
        if o_i.cart_id:
            cart = Cart.objects.get(id=o_i.cart_id)
            cart.delete()
        cloth = Cloth.objects.get(id=o_i.cloth_id)
        cloth.sales += o_i.goods_number
        cloth.save()
    return redirect("/customer/shop/")
