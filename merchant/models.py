from django.db import models


# Create your models here.
class Banner(models.Model):
    title = models.TextField()
    description = models.TextField()
    state = models.IntegerField(default=1)
    picture = models.ImageField(upload_to="customer/img/banner")
    url = models.TextField()
