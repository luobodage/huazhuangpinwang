from django.contrib import admin
from .models import *


# Register your models here.

class DataAdmin(admin.ModelAdmin):
    list_display = ('shop_price', 'shop_title', 'shop_category_1', 'shop_category_2', 'shop_brand')


admin.site.register(Data, DataAdmin)
