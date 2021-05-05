from django.db import models


# Create your models here.
class Data(models.Model):
    shop_price = models.CharField(max_length=20, verbose_name='商品价格')
    shop_title = models.CharField(max_length=100, verbose_name='商品标题')
    shop_category_1 = models.CharField(max_length=20, verbose_name='商品品类1')
    shop_category_2 = models.CharField(max_length=20, verbose_name='商品品类2')
    shop_brand = models.CharField(max_length=50, verbose_name='商品品牌')
    suitableForSkinType = models.CharField(max_length=50, verbose_name='适合肤质')
    howManyPeopleWantToUse = models.CharField(max_length=20, verbose_name='多少人想用')
    howManyPeopleLikeToUseIt = models.CharField(max_length=20, verbose_name='多少人爱用')
    howManyComments = models.CharField(max_length=20, verbose_name='多少人评论')
    shop_comment = models.TextField(verbose_name='评论')


class ShowData(Data):
    class Meta():
        proxy = True  # 使用代理
        verbose_name = "化妆品网商品数据展示"
        verbose_name_plural = verbose_name


class JiaQian(Data):
    class Meta():
        proxy = True  # 使用代理
        verbose_name = "品牌数量与时间比例大数据柱图"
        verbose_name_plural = verbose_name


class DiZhi(Data):
    class Meta():
        proxy = True
        verbose_name = "价格区间统计"
        verbose_name_plural = verbose_name


class ShouMai(Data):
    class Meta():
        proxy = True  # 使用代理
        verbose_name = "化妆品品牌分布饼图"
        verbose_name_plural = verbose_name


class QiShou(Data):
    class Meta():
        proxy = True  # 使用代理
        verbose_name = "商品主要功能与数量对比散点图"
        verbose_name_plural = verbose_name



class GcJq(Data):
    class Meta():
        proxy = True
        verbose_name = "品牌前五多少人想要、喜欢、评论"
        verbose_name_plural = verbose_name
