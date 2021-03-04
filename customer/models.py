from django.db import models


# Create your models here.
class Pinlei(models.Model):
    pinlei = models.IntegerField(blank=True, null=True)


class Fenlei(models.Model):
    fenlei = models.CharField(max_length=32)
    pinlei = models.ForeignKey(to=Pinlei, on_delete=models.CASCADE)


class Cloth(models.Model):
    # 标题
    title = models.TextField()
    # 价格
    price = models.FloatField()
    # 货号
    coodsNo = models.CharField(max_length=32)
    # 重量
    weight = models.FloatField()
    # 上架日期
    date = models.DateField(auto_now=True)
    # 图片
    # picture = models.ImageField(upload_to="customer/img/clothes", max_length=128)
    picture = models.TextField()
    # 优惠价
    discount_price = models.FloatField(default=0)
    # 颜色
    color = models.TextField()
    # 状态
    state = models.IntegerField(default=1)
    # 数量
    number = models.IntegerField()
    # 销量
    sales = models.IntegerField(default=500)
    # 分类
    fenlei = models.ForeignKey(to=Fenlei, on_delete=models.CASCADE)
    # 品类
    pinlei = models.ForeignKey(to=Pinlei, on_delete=models.CASCADE)
