from django.contrib import admin
from .models import *


# Register your models here.

class ClothAdmin(admin.ModelAdmin):
    list_display = ("title",)
    list_filter = ("state",)


class FenleiAdmin(admin.ModelAdmin):
    list_display = ("fenlei",)
    # model = Fenlei
    # extra = 2


class PinleiAdmin(admin.ModelAdmin):
    list_display = ("pinlei",)
    # inlines = [FenleiAdmin]

admin.site.register(Cloth, ClothAdmin)
admin.site.register(Pinlei, PinleiAdmin)
admin.site.register(Fenlei, FenleiAdmin)
