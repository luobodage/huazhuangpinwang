from collections import Counter

from django.contrib import admin
from .models import *
from app.models import Data
from .models import *
import pandas
import numpy as np

# Register your models here.

# class DataAdmin(admin.ModelAdmin):
#     list_display = ('shop_price', 'shop_title', 'shop_category_1', 'shop_category_2', 'shop_brand')
#
#
# admin.site.register(Data, DataAdmin)
data = pandas.read_csv("static/app_data.csv")
# 存在空值，去掉
data = data.dropna(subset=['id'])
data = data.dropna(subset=['shop_price'])
data = data.dropna(subset=['shop_title'])
data = data.dropna(subset=['shop_category_1'])
data = data.dropna(subset=['shop_category_2'])
data = data.dropna(subset=['shop_brand'])
data = data.dropna(subset=['suitableForSkinType'])
data = data.dropna(subset=['howManyPeopleWantToUse'])
data = data.dropna(subset=['howManyPeopleLikeToUseIt'])
data = data.dropna(subset=['howManyComments'])
data = data.dropna(subset=['shop_comment'])
# 把价格改成浮点型
data['shop_price'] = data['shop_price'].astype('float')

# 去空格
data['shop_title'] = data['shop_title'].str.replace(' ', '')

# Register your models here.
admin.AdminSite.site_header = '化妆品网数据采集系统'
admin.AdminSite.site_title = '化妆品网数据采集系统'


class ShowDataAdmin(admin.ModelAdmin):

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context
        )
        data_temp = data.groupby(pandas.cut(data['shop_price'], np.arange(0, 10000, 1000))).count()
        data1 = []
        type = []
        for index, row in data_temp.iterrows():
            data1.append(row['shop_price'])
            type.append(str(index) + "元")
        response.context_data['type'] = type
        response.context_data['data1'] = data1
        price1 = zip(type, data1)
        price = []
        for i in price1:
            list01 = list(i)
            price.append(list01)
        response.context_data['price'] = price

        return response


admin.site.register(ShowData, ShowDataAdmin)


class JiaQianAdmin(admin.ModelAdmin):
    list_per_page = 2099

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context
        )
        data_temp = data.groupby(pandas.cut(data['shop_price'], np.arange(0, 100, 10))).count()
        data1 = []
        type = []
        for index, row in data_temp.iterrows():
            data1.append(row['shop_title'])
            type.append(str(index) + "元")
        response.context_data['type'] = type
        response.context_data['data1'] = data1
        price1 = zip(type, data1)
        price = []
        for i in price1:
            list01 = list(i)
            price.append(list01)
        response.context_data['price'] = price

        return response


class DiZhiAdmin(admin.ModelAdmin):
    list_per_page = 2100

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context
        )
        data_temp = data.groupby(pandas.cut(data['shop_price'], np.arange(0, 100, 10))).count()
        data1 = []
        type = []
        for index, row in data_temp.iterrows():
            data1.append(row['shop_title'])
            type.append(str(index) + "元")
        response.context_data['type'] = type
        response.context_data['data1'] = data1
        price1 = zip(type, data1)
        price = []
        for i in price1:
            list01 = list(i)
            price.append(list01)
        response.context_data['price'] = price

        return response


class ShouMaiAdmin(admin.ModelAdmin):
    list_per_page = 2484

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context
        )
        data_temps = data["shop_brand"].tolist()
        res = dict(Counter(data_temps))
        res1 = sorted(res.items(), key=lambda item: item[1], reverse=False)[:12]
        data1 = []
        leng = []
        # keys与values分别为该数据的键数组，值的数组。这里循环为字典添加对应键值
        for k, v in res1:
            data1.append({"value": v, "name": str(k)})
            leng.append(str(k))

        response.context_data['data1'] = data1
        response.context_data['leng'] = leng
        return response


class QiShouAdmin(admin.ModelAdmin):
    list_per_page = 2484

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context
        )
        data_temp = data.groupby(data['shop_category_1']).count()
        data1 = []
        type = []
        for index, row in data_temp.iterrows():
            data1.append(row['shop_title'])
            type.append(str(index))
        response.context_data['type'] = type
        response.context_data['data1'] = data1
        return response


class GcJqAdmin(admin.ModelAdmin):
    list_per_page = 2099

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context
        )
        data_temp = data.groupby(data['shop_brand']).count()
        data1 = []
        type = []
        for index, row in data_temp.iterrows():
            data1.append(row['shop_title'])
            type.append(str(index))
        response.context_data['type'] = type
        response.context_data['data1'] = data1
        return response





admin.site.register(JiaQian, JiaQianAdmin)
admin.site.register(ShouMai, ShouMaiAdmin)
admin.site.register(QiShou, QiShouAdmin)

admin.site.register(DiZhi, DiZhiAdmin)
admin.site.register(GcJq, GcJqAdmin)
