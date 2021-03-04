import time

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from customer.models import *
from User.models import User, Cart, PayOrder, History, UserAddress, OrderInfo
from User.views import valid_user, set_password, valid_login
from merchant.models import Banner
from User.views import valid_cookie


# Create your views here.


def index(request):
    account = request.COOKIES.get("account")
    user = valid_user(account)
    banners = Banner.objects.filter(state=1)
    cloth_list = Cloth.objects.order_by("-sales")[:8]
    female_new = Cloth.objects.filter(pinlei=2, state=1).order_by("-date")[:6]
    male_new = Cloth.objects.filter(pinlei=1, state=1).order_by("-date")[:6]
    return render(request, "customer/index.html", locals())


def login(request):
    msg = ""
    next = request.GET.get("next", "")
    if request.method == "POST":
        account = request.POST.get("account")
        pwd = request.POST.get("password")
        admin = request.POST.get("admin")
        next = request.POST.get("next")
        if admin == "on":
            user = valid_user(account)
            if user.identity == 1:
                if user.password == set_password(pwd):
                    response = redirect("/merchant/")
                    response.set_cookie("account", user.account)
                    response.set_cookie("user_id", user.id)
                    request.session["account"] = user.account
                    return response
                else:
                    msg = "账号或密码错误！"
            else:
                msg = "该用户不是管理员"
        else:
            user = valid_user(account)
            if user:
                if set_password(pwd) == user.password:
                    if next:
                        if next.startswith("/"):
                            response = redirect(next)
                        else:
                            response = redirect("/" + next)
                    else:
                        response = redirect("/")
                    response.set_cookie("account", user.account)
                    response.set_cookie("user_id", user.id)
                    request.session["account"] = user.account
                    return response
                else:
                    msg = "账号或密码错误！"
            else:
                msg = "该账号未被注册"
    return render(request, "customer/login.html", locals())


def shop(request):
    pl = request.GET.get("pinlei", "male")
    key = request.GET.get("key", None)
    banners = Banner.objects.filter(state=1)
    if not key:
        if "_" in pl:
            data = pl.split("_")
            pl = data[0]
            kind = int(data[1])
            if kind != 0:
                clothes = Cloth.objects.filter(fenlei=kind, state=1)
            else:
                if pl == "male":
                    clothes = Cloth.objects.filter(pinlei=1, state=1)
                else:
                    clothes = Cloth.objects.filter(pinlei=2, state=1)
        else:
            kind = 0
            if pl == "male":
                clothes = Cloth.objects.filter(pinlei=1, state=1)
            else:
                clothes = Cloth.objects.filter(pinlei=2, state=1)
    else:
        clothes = Cloth.objects.filter(title__contains=key, state=1)
        if not clothes:
            try:
                fl = Fenlei.objects.get(fenlei__contains=key)
            except:
                fl = None
            clothes = Cloth.objects.filter(fenlei=fl, state=1)
            if len(clothes) == 0:
                nothing = True
    pinlei = Pinlei.objects.all()
    if pl == "male":
        fenlei = Fenlei.objects.filter(pinlei=1)
    else:
        fenlei = Fenlei.objects.filter(pinlei=2)
    page_number = int(request.GET.get("page", "1"))
    paginator = Paginator(clothes, 40)
    clothes = paginator.page(page_number)
    page_long = len(list(paginator.page_range))
    if page_number >= 59:
        page_range = list(paginator.page_range)[58:]
    else:
        page_range = list(paginator.page_range)[int(page_number) - 1:int(page_number) + 5]
    first = list(paginator.page_range)[0]
    last = list(paginator.page_range)[-1]
    # print(page_number, page_long)
    return render(request, "customer/shop.html", locals())


def detail(request, id):
    cloth = Cloth.objects.get(id=int(id))
    split = "," if "," in cloth.color else "，"
    colors = cloth.color.split(split)
    account = request.COOKIES.get("account")
    pictures = cloth.picture.split(",")[:6]
    if account:
        user = valid_user(account)
        his = History.objects.filter(user_id=user.id)
        his_id = [i.goods_id for i in his]
        if len(his) > 7 and int(id) not in his_id:
            his[0].delete()
        if int(id) not in his_id:
            history = History()
            history.user_id = valid_user(account)
            history.goods_id = cloth.id
            history.goods_name = cloth.title
            history.goods_price = str(cloth.price) + "," + str(cloth.discount_price) if cloth.discount_price else str(
                cloth.price)
            history.goods_picture = cloth.picture.split(",")[0]
            history.save()
    if request.method == "POST":
        account = request.COOKIES.get("account", None)
        user = valid_user(account)
        if user:
            # 获取Post提交的数据
            color = request.POST.get("color")
            size = request.POST.get("size")
            number = request.POST.get("number")
            cloth_id = request.POST.get("cloth_id")
            cloth = Cloth.objects.get(id=int(cloth_id))
            price = cloth.discount_price if cloth.discount_price > 0 else cloth.price
            # 生成订单
            order = PayOrder()
            order.order_number = str(time.time()).replace(".", "")
            order.order_total = int(number) * price
            order.order_user = user
            order.order_address = user.useraddress_set.get(state=1).address \
                if user.useraddress_set.get(state=1) else user.useraddress_set.first().address
            order.save()
            # 保存订单详情
            order_info = OrderInfo()
            order_info.goods_name = cloth.title
            order_info.goods_number = int(number)
            order_info.goods_price = price
            order_info.goods_total = int(number) * price
            if "," in cloth.picture:
                order_info.goods_picture = cloth.picture.split(",")[0]
            else:
                order_info.goods_picture = cloth.picture.split("，")[0]
            order_info.order_id = order
            order_info.goods_color = color
            order_info.goods_size = size
            order_info.cloth_id = cloth.id
            order_info.save()
            return redirect(f"/user/place_order/?order_id={order.id}")
        else:
            return redirect(f"/login/?next=/customer/detail/{id}")
    return render(request, "customer/detail.html", locals())


@valid_login
@valid_cookie
def user_center_info(request):
    msg = "修改信息"
    account = request.COOKIES.get("account")
    user = valid_user(account)
    try:
        address = user.useraddress_set.get(state=1)
    except:
        address = user.useraddress_set.filter(state=0).first()
    history = History.objects.filter(user_id=user.id).order_by("-id")
    return render(request, "customer/user_center_info.html", locals())


@valid_login
@valid_cookie
def changeinfo(request):
    change = True
    msg = "确认修改"
    account = request.COOKIES.get("account")
    user = valid_user(account)
    history = History.objects.filter(user_id=user.id).order_by("-id")
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        user.name = name
        user.phone = phone
        user.address = address
        user.save()
        return redirect("/customer/ucf/")
    return render(request, "customer/user_center_info.html", locals())


@valid_login
def user_center_order(request):
    key = request.GET.get("key", None)
    page_number = int(request.GET.get("page", "1"))
    account = request.COOKIES.get("account")
    user = valid_user(account)
    if not key:
        order_list = PayOrder.objects.filter(order_user=user.id).order_by("-order_time")
    else:
        order_list = PayOrder.objects.filter(order_number=key)
        if len(order_list) == 0:
            nothing = True
            order_list = PayOrder.objects.filter(order_user=user.id).order_by("-order_time")
    paginator = Paginator(order_list, 10)
    order_list = paginator.page(page_number)
    page_long = len(list(paginator.page_range))
    if page_number >= page_long:
        page_range = list(paginator.page_range)[page_long:]
    else:
        page_range = list(paginator.page_range)[page_number - 1:page_number + 5]
    first = list(paginator.page_range)[0]
    last = list(paginator.page_range)[-1]
    return render(request, "customer/user_center_order.html", locals())


@valid_login
def user_center_site(request):
    account = request.COOKIES.get("account")
    user = valid_user(account)
    address = user.useraddress_set.all()
    try:
        default_address = user.useraddress_set.get(state=1)
    except:
        pass
    other_address = user.useraddress_set.filter(state=0)
    if request.method == "POST":
        receiver = request.POST.get("rec")
        post_address = request.POST.get("address")
        post_code = request.POST.get("post_code")
        phone = request.POST.get("phone")
        if len(phone) != 11:
            msg = "手机号格式不正确"
        else:
            address = UserAddress()
            address.receiver = receiver
            address.address = post_address
            address.post_number = post_code
            address.phone = phone
            address.user = user
            address.save()
            return HttpResponseRedirect("/customer/ucs/")
    return render(request, "customer/user_center_site.html", locals())


@valid_login
def change_address(request, id):
    account = request.COOKIES.get("account")
    user = valid_user(account)
    address = user.useraddress_set.all()
    try:
        default_address = user.useraddress_set.get(state=1)
    except:
        pass
    other_address = user.useraddress_set.filter(state=0)
    old_address = UserAddress.objects.get(id=int(id))
    if request.method == "POST":
        receiver = request.POST.get("rec")
        post_address = request.POST.get("address")
        post_code = request.POST.get("post_code")
        phone = request.POST.get("phone")
        # print(receiver, post_address, phone, post_code)
        if len(phone) != 11:
            msg = "手机号格式不正确"
        else:
            old_address.receiver = receiver
            old_address.address = post_address
            old_address.post_number = post_code
            old_address.phone = phone
            old_address.save()
            return HttpResponseRedirect("/customer/ucs/")
    return render(request, "customer/change_address.html", locals())


def setdefault(request):
    result = {"state": "error", "data": ""}
    if request.method == "POST":
        id = request.POST.get("id")
        try:
            old = UserAddress.objects.get(state=1)
            old.state = 0
            old.save()
        except:
            pass
        new_address = UserAddress.objects.get(id=int(id))
        new_address.state = 1
        new_address.save()
        result["state"] = "success"
        result["data"] = "设置成功"
        return JsonResponse(result)


def delete(request):
    result = {"state": "error", "data": ""}
    if request.method == "POST":
        id = request.POST.get("id")
        old = UserAddress.objects.get(id=int(id))
        old.delete()
        result["state"] = "success"
        result["data"] = "删除成功"
        return JsonResponse(result)
