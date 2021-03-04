from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.http import JsonResponse
# Create your views here.
from User.models import PayOrder
from customer.models import Cloth, Pinlei, Fenlei
from merchant.models import Banner
from User.views import valid_cookie


@valid_cookie
def list_goods(request):
    pl = request.GET.get("pinlei", "male")
    page_number = int(request.GET.get("page", "1"))
    key = request.GET.get("key", None)
    if not key:
        if "_" in pl:
            page_size = 50
            data = pl.split("_")
            pl = data[0]
            kind = int(data[1])
            if kind != 0:
                clothes = Cloth.objects.filter(fenlei=kind)
            else:
                if pl == "male":
                    clothes = Cloth.objects.filter(pinlei=1)
                else:
                    clothes = Cloth.objects.filter(pinlei=2)
        else:
            kind = 0
            page_size = 100
            if pl == "male":
                clothes = Cloth.objects.filter(pinlei=1)
            else:
                clothes = Cloth.objects.filter(pinlei=2)
    else:
        page_size = 1
        clothes = Cloth.objects.filter(title__contains=key)
    pinlei = Pinlei.objects.all()
    if pl == "male":
        fenlei = Fenlei.objects.filter(pinlei=1)
    else:
        fenlei = Fenlei.objects.filter(pinlei=2)
    paginator = Paginator(clothes, page_size)
    clothes = paginator.page(str(page_number))
    page_long = len(list(paginator.page_range))
    if page_number >= page_long:
        page_range = list(paginator.page_range)[page_long:]
    else:
        page_range = list(paginator.page_range)[page_number - 1:page_number + 5]
    first = list(paginator.page_range)[0]
    last = list(paginator.page_range)[-1]
    return render(request, "merchant/list_goods.html", locals())


@valid_cookie
def set_state(request, id):
    type = request.GET.get("type")
    if type == "cloth":
        cloth = Cloth.objects.get(id=int(id))
        if cloth.state == 1:
            cloth.state = 0
        else:
            cloth.state = 1
        cloth.save()
        HTTP_REFERER = request.META.get("HTTP_REFERER")
        referer = HTTP_REFERER.split("/", 3)[-1]
        return redirect("/" + referer)
    elif type == "banner":
        banner = Banner.objects.get(id=int(id))
        if banner.state == 1:
            banner.state = 0
        else:
            banner.state = 1
        banner.save()
        return redirect("/merchant/banner")


@valid_cookie
def add_goods(request):
    msg = "添加商品"
    add = True
    pinlei = Pinlei.objects.all()
    if request.method == "POST":
        title = request.POST.get("title")
        price = request.POST.get("price")
        color = request.POST.get("color")
        code = request.POST.get("code")
        weight = request.POST.get("weight")
        number = request.POST.get("number")
        date = request.POST.get("date")
        discount = request.POST.get("discount")
        state = request.POST.get("state")
        pl = request.POST.get("pinlei")
        fl = request.POST.get("fenlei")
        picture = request.POST.get("picture")
        if title and price and color and number and code and weight and pl and fl:
            cloth = Cloth()
            cloth.title = title
            cloth.price = float(price)
            cloth.number = float(number)
            cloth.coodsNo = code
            cloth.weight = weight
            cloth.date = date
            cloth.discount_price = discount
            cloth.state = state
            cloth.pinlei = Pinlei.objects.get(id=int(pl))
            cloth.fenlei = Fenlei.objects.get(id=int(fl))
            cloth.picture = picture
            cloth.save()
            msg2 = "添加成功"
        else:
            msg1 = "请完善商品信息"
    return render(request, "merchant/com_goods.html", locals())


@valid_cookie
def change(request, id):
    type = request.GET.get("type")
    if type == "cloth":
        change = True
        msg = "确认修改商品信息"
        cloth = Cloth.objects.get(id=int(id))
        pinlei = Pinlei.objects.all()
        if request.method == "POST":
            title = request.POST.get("title")
            price = request.POST.get("price")
            number = request.POST.get("number")
            date = request.POST.get("date")
            discount = request.POST.get("discount")
            state = request.POST.get("state")
            pl = request.POST.get("pinlei")
            fl = request.POST.get("fenlei")
            picture = request.POST.get("picture")
            if title and price and number and date and pl and fl:
                cloth.title = title
                cloth.price = float(price)
                cloth.number = float(number)
                cloth.date = date
                cloth.discount_price = discount
                cloth.state = state
                cloth.pinlei = Pinlei.objects.get(id=int(pl))
                cloth.fenlei = Fenlei.objects.get(id=int(fl))
                cloth.picture = picture
                cloth.save()
                return redirect(f"/customer/detail/{id}")
            else:
                msg1 = "请完善商品信息"
        return render(request, "merchant/com_goods.html", locals())
    elif type == "banner":
        msg = "确认修改"
        banners = Banner.objects.all()
        banner = Banner.objects.get(id=int(id))
        if request.method == "POST":
            title = request.POST.get("title")
            des = request.POST.get("des")
            url = request.POST.get("url")
            picture = request.FILES.get("picture")
            # print(title, des, url, picture)
            if title and des and url and picture:
                banner.title = title
                banner.description = des
                banner.url = url
                banner.picture = picture
                banner.save()
                redirect("/merchant/banner")
            else:
                msg1 = "请完善数据"

        return render(request, "merchant/banner_manage.html", locals())


def get_fenlei(request):
    result = {"state": "error", "data": ""}
    if request.method == "POST":
        pinlei_id = request.POST.get("pinlei_id")
        fenlei = Fenlei.objects.filter(pinlei_id=int(pinlei_id))
        result["state"] = "success"
        result["data"] = [(f.fenlei, f.id) for f in fenlei]
    return JsonResponse(result)


@valid_cookie
def orderManage(request):
    key = request.GET.get("key", None)
    page_number = int(request.GET.get("page", "1"))
    if key:
        order_list = PayOrder.objects.filter(order_number=key)
        if len(order_list) == 0:
            nothing = True
            order_list = PayOrder.objects.all().order_by("-order_time")
    else:
        order_list = PayOrder.objects.all().order_by("-order_time")
    if len(order_list) <= 10:
        page_size = 7
    else:
        page_size = 10
    paginator = Paginator(order_list, page_size)
    order_list = paginator.page(str(page_number))
    page_long = len(list(paginator.page_range))
    if page_number >= page_long:
        page_range = list(paginator.page_range)[page_long:]
    else:
        page_range = list(paginator.page_range)[page_number - 1:page_number + 5]
    first = list(paginator.page_range)[0]
    last = list(paginator.page_range)[-1]
    return render(request, "merchant/order_manage.html", locals())


@valid_cookie
def order_state(request, id):
    operation = request.GET.get("operation")
    order = PayOrder.objects.get(id=int(id))
    if operation == "send":
        order.order_state = 2
        order.save()
        return redirect("/merchant/ordermanage")


@valid_cookie
def bannerManage(request):
    msg = "确认添加"
    banners = Banner.objects.all()
    if request.method == "POST":
        title = request.POST.get("title")
        des = request.POST.get("des")
        url = request.POST.get("url")
        picture = request.FILES.get("picture")
        if title or des or url or picture:
            banner = Banner()
            banner.title = title
            banner.description = des
            banner.url = url
            banner.picture = picture
            banner.save()
            redirect("/merchant/banner")
        else:
            msg1 = "不能全部为空"
    return render(request, "merchant/banner_manage.html", locals())


@valid_cookie
def delbanner(request, id):
    banner = Banner.objects.get(id=int(id))
    banner.delete()
    return redirect("/merchant/banner")


@valid_cookie
def sales_analysis(request):
    male = Cloth.objects.filter(pinlei=1).aggregate(male_sum=Sum("sales"))
    female = Cloth.objects.filter(pinlei=2).aggregate(female_sum=Sum("sales"))
    male_sum = male["male_sum"]
    female_sum = female["female_sum"]
    return render(request, "merchant/sales_analysis.html", locals())


def analysis_data(request):
    result = {"state": "error", "male": {}, "female": {}}
    data = Cloth.objects.values("fenlei").annotate(Sum("sales"))
    # print(data)
    fenlei_list = Fenlei.objects.all()
    male_fenlei = {}
    female_fenlei = {}
    for i in fenlei_list:
        if i.pinlei_id == 1:
            male_fenlei[i.id] = 0
        elif i.pinlei_id == 2:
            female_fenlei[i.id] = 0
    for i in data:
        if i["fenlei"] in male_fenlei.keys():
            male_fenlei[i["fenlei"]] = i["sales__sum"]
        elif i["fenlei"] in female_fenlei.keys():
            female_fenlei[i["fenlei"]] = i["sales__sum"]
    for i in fenlei_list:
        if i.id in male_fenlei.keys():
            male_fenlei[i.fenlei] = male_fenlei.pop(i.id)
        elif i.id in female_fenlei.keys():
            female_fenlei[i.fenlei] = female_fenlei.pop(i.id)
    # print(male_fenlei)
    # print(female_fenlei)
    result["state"] = "success"
    result["male"] = male_fenlei
    result["female"] = female_fenlei
    return JsonResponse(result)
