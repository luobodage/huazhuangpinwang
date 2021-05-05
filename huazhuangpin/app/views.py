import pandas as pd
from django.shortcuts import render
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.charts import Pie
from pyecharts.charts import Scatter
import jieba
from app.models import *

"""
数据预处理
"""
mysql_data = Data.objects.all().values()
df = pd.DataFrame(mysql_data)
df = df[~(df['shop_price'].isin(['0.0']))]  # 去掉价格为0.0的多与数据
row = df.index.size  # 数据量

# 对商品品牌进行分组
shop_data = df.groupby("shop_brand", as_index=False).agg(
    count=pd.NamedAgg(column="id", aggfunc="count", ))
shop_data = shop_data.sort_values(by="count", ascending=False)  # 排序
shop_brand_list = list(shop_data['shop_brand'][:10])
print(shop_brand_list)

# 对商品功能进行分组 1
shop_category_1 = df.groupby("shop_category_1", as_index=False).agg(
    count=pd.NamedAgg(column="id", aggfunc="count", ))
shop_category_1 = shop_category_1.sort_values(by="count", ascending=False)
shop_category_1_list = list(shop_category_1['shop_category_1'][:10])
print(shop_category_1_list)

# 对商品功能进行分组 2
shop_category_2 = df.groupby("shop_category_2", as_index=False).agg(
    count=pd.NamedAgg(column="id", aggfunc="count", ))
shop_category_2 = shop_category_2.sort_values(by="count", ascending=False)
shop_category_2_list = list(shop_category_2['shop_category_2'][:10])
# print(shop_category_2_list)

howManyPeopleWantToUse_mean = df['howManyPeopleWantToUse'].astype(int).mean()
howManyPeopleLikeToUseIt_meam = df['howManyPeopleLikeToUseIt'].astype(int).mean()
howManyComments_mean = df['howManyComments'].astype(int).mean()
shop_quantity = df['shop_comment'].index.size
shop_comment = list(df['shop_comment'][1:2])
shop_title = list(df['shop_title'][1:2])
a = ','.join(shop_comment)
b = a.split('...,')
"""
数据预处理结束
"""
"""
生成分析图
"""



def line_html():
    """
    通过数据库数据进行读取数据
    生成line图 根据商品品牌
    :return: 返回一个html文件
    """
    all_data = []
    for row in shop_data.itertuples():
        # now_name 为列名
        a = [getattr(row, 'shop_brand'), getattr(row, 'count')]

        all_data.append(a)

    (
        Line(init_opts=opts.InitOpts(width="1680px", height="800px"))
            .add_xaxis(xaxis_data=[item[0] for item in all_data])
            .add_yaxis(
            series_name="",
            y_axis=[item[1] for item in all_data],
            yaxis_index=0,
            is_smooth=True,
            is_symbol_show=False,
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="化妆品品牌主要分布"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            datazoom_opts=[
                opts.DataZoomOpts(yaxis_index=0),
                opts.DataZoomOpts(type_="inside", yaxis_index=0),
            ],
            visualmap_opts=opts.VisualMapOpts(
                pos_top="10",
                pos_right="10",
                is_piecewise=True,
                pieces=[
                    {"gt": 0, "lte": 1, "color": "#096"},
                    {"gt": 1, "lte": 2, "color": "#ffde33"},
                    {"gt": 3, "lte": 4, "color": "#ff9933"},
                    {"gt": 5, "lte": 6, "color": "#cc0033"},
                    {"gt": 7, "lte": 8, "color": "#660099"},
                    {"gt": 10, "color": "#7e0023"},
                ],
                out_of_range={"color": "#999"},
            ),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name_location="start",
                min_=0,
                max_=10,
                is_scale=True,
                axistick_opts=opts.AxisTickOpts(is_inside=False),
            ),
        )
            .set_series_opts(
            markline_opts=opts.MarkLineOpts(
                data=[
                    {"yAxis": 1},
                    {"yAxis": 2},
                    {"yAxis": 3},
                    {"yAxis": 4},
                    {"yAxis": 10},
                ],
                label_opts=opts.LabelOpts(position="end"),
            )
        )
            .render("./templates/line.html")
    )


def pie_html():
    """
    生成饼图 通过产品的主要功效
    :return:
    """
    c = (
        Pie(init_opts=opts.InitOpts(width="1800px", height="800px"))
            .add(
            "",
            [
                list(z)
                for z in zip(
                shop_category_1['shop_category_1'][:20],
                shop_category_1['count'][:20]
            )
            ],
            center=["40%", "50%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="化妆品主要功能分布数据"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .render("./templates/pie.html")
    )


# 传入前端的数据
data = {
    'row': row,
    'shop_brand': shop_brand_list,
    'shop_category_1_list': shop_category_1_list,
    'shop_category_2_list': shop_category_2_list,
    'howManyPeopleWantToUse': int(howManyPeopleWantToUse_mean),
    'howManyPeopleLikeToUseIt': int(howManyPeopleLikeToUseIt_meam),
    'howManyComments': int(howManyComments_mean),
    'shop_quantity': shop_quantity,
    'shop_comment': b,
    'shop_title': shop_title,

}


def scatter_html():
    """
    生成散点图 根据产品的喜爱程度
    :return:
    """
    c = (
        Scatter(init_opts=opts.InitOpts(width="1800px", height="800px"))
            .add_xaxis(list(df['shop_title'][:50]))
            .add_yaxis("产品名称", list(df['howManyPeopleLikeToUseIt'][:50]))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="各大产品喜爱程度散点图"),
            xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
        )
            .render("./templates/scatter.html")
    )


# Create your views here.
def app(request):
    return render(request, 'index.html', data)


def line(request):
    line_html()
    return render(request, 'line.html')


def pie(request):
    pie_html()
    return render(request, 'pie.html')


def scatter(request):
    scatter_html()
    return render(request, 'scatter.html')
