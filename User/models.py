from django.db import models


# Create your models here.

class User(models.Model):
    account = models.CharField(max_length=32)
    name = models.CharField(max_length=32, default="123")
    password = models.CharField(max_length=32)
    email = models.EmailField()
    phone = models.CharField(max_length=32)
    address = models.TextField(blank=True, null=True)
    identity = models.IntegerField(default=0)


class Cart(models.Model):
    user_id = models.IntegerField()
    name = models.TextField()
    price = models.FloatField()
    color = models.CharField(max_length=16)
    size = models.CharField(max_length=16)
    number = models.IntegerField()
    picture = models.TextField()
    total = models.FloatField()
    cloth_id = models.IntegerField()


class PayOrder(models.Model):
    """
    订单状态：
    0：未支付
    1：已支付未发货
    2：已发货待收货
    3：代签收
    4：拒收
    """
    order_number = models.CharField(max_length=32)
    order_time = models.DateTimeField(auto_now=True)
    order_total = models.FloatField(default=0)
    order_state = models.IntegerField(default=0)
    order_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    order_address = models.TextField()


class OrderInfo(models.Model):
    order_id = models.ForeignKey(to=PayOrder, on_delete=models.CASCADE)
    goods_name = models.TextField()
    goods_number = models.IntegerField()
    goods_price = models.FloatField()
    goods_total = models.FloatField(default=0)
    goods_picture = models.TextField()
    goods_color = models.CharField(max_length=32)
    goods_size = models.CharField(max_length=32)
    cart_id = models.IntegerField(blank=True, null=True)
    cloth_id = models.IntegerField(blank=True, null=True)


class History(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    goods_id = models.IntegerField()
    goods_name = models.TextField()
    goods_price = models.CharField(max_length=16)
    goods_picture = models.TextField()


class UserAddress(models.Model):
    receiver = models.CharField(max_length=64)
    address = models.TextField(blank=True, null=True)
    post_number = models.CharField(max_length=32, blank=True, null=True)
    phone = models.CharField(max_length=32)
    state = models.IntegerField(default=0)  # 0常规地址 1默认地址
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
