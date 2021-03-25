# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import create_engine
import pandas as pd
from huazhuangpin.items import HuazhuangpinItem
import pymysql

connect = create_engine('mysql+pymysql://root:1334@127.0.0.1:3306/huazhuangpin?charset=utf8')


class HuazhuangpinPipeline:
    def __init__(self):
        # 1. 建立数据库的连接
        self.connect = pymysql.connect(
            # localhost连接的是本地数据库
            host='localhost',
            # mysql数据库的端口号
            port=3306,
            # 数据库的用户名
            user='root',
            # 本地数据库密码
            passwd='1334',
            # 表名
            db='huazhuangpin',
            # 编码格式
            charset='utf8'
        )
        # 2. 创建一个游标cursor, 是用来操作表。
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # 3. 将Item数据放入数据库，默认是同步写入。
        insert_sql = "INSERT INTO hzp_data(商品价格, 商品名称, 产品品类1, 产品品类2,商品品牌,适合肤质,多少人想用,多少人爱用,多少评论,评论内容) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
            item['shop_price'], item['shop_title'], item['shop_category_1'], item['shop_category_2'],
            item['shop_brand'], item['shop_fuzhi'], item['shop_like'], item['shop_love'], item['shop_comment_amount'],
            item['shop_comment'])
        self.cursor.execute(insert_sql)

        # 4. 提交操作
        self.connect.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
    # def process_item(self, item, spider):
    #     data = pd.DataFrame()
    #     data['商品价格'] = item['shop_price']
    #     data['商品名称'] = item['shop_title']
    #     data['产品品类1'] = item['shop_category_1']
    #     data['产品品类2'] = item['shop_category_2']
    #     data['商品品牌'] = item['shop_brand']
    #     data['适合肤质'] = item['shop_fuzhi']
    #     data['多少人想用'] = item['shop_like']
    #     data['多少人爱用'] = item['shop_love']
    #     data['多少评论'] = item['shop_comment_amount']
    #     data['评论内容'] = item['shop_comment']
    #     data.to_sql('hzp_data', con=connect.engine, if_exists='append', index=False)
    #     print(data.head())
    #     return item
