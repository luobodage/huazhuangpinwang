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
