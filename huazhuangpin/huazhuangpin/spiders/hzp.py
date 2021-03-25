import scrapy
from huazhuangpin.items import HuazhuangpinItem

item = HuazhuangpinItem()


class HzpSpider(scrapy.Spider):
    name = 'hzp'
    allowed_domains = ['hzp.onlylady.com']
    start_urls = ['http://hzp.onlylady.com/brand.html']

    def parse(self, response, **kwargs):
        """
        第一个页面 获取每一个品牌的链接地址
        :param response: 内容信息
        :param kwargs:
        """
        # 店地址
        hzp_href = response.xpath('//dl[@class=\'brandsWraper\']/dd/div/div[2]/a/@href').extract()
        print(hzp_href)
        # 店标题
        hzp_title = response.xpath('//dl[@class=\'brandsWraper\']/dd/div/div[2]/a/@href').extract()
        for index, href in enumerate(hzp_href):
            # item['hzp_href'] = href
            # item['hzp_title'] = hzp_title[index]
            print(href)
            yield scrapy.Request(url=href, callback=self.parse1)
        # return item
        # item['hzp_href'] = hzp_href
        # item['hzp_title'] = hzp_title

    def parse1(self, response, **kwargs):
        """
        获取这个化妆品店的列表
        :param response:
        :param kwargs:
        :return:
        """
        # hzp_title = response.meta['hzp_title']

        shop_list_href = response.xpath("//div[@class='tt_1']/a/@href").extract_first()
        print(shop_list_href)
        yield scrapy.Request(url=shop_list_href, callback=self.parse2)
        # item['hzp_title'] = hzp_title

    def parse2(self, response, **kwargs):
        """
        获取这个商品的详细信息地址
        :param response:
        :param kwargs:
        :return:
        """
        shop_href = response.xpath("//div[@class='commentBody']/h4/a/@href").extract()
        shop_price = response.xpath("//div[@class='commentBrief']/p[2]/span[2]/text()").extract()
        for index, href in enumerate(shop_href):
            print(href)
            yield scrapy.Request(url=href, callback=self.parse3, meta={'shop_price': shop_price[index][1:]})

    def parse3(self, response, **kwargs):
        """
        获取商品信息
        :param response:
        :param kwargs:
        :return:
        """
        # 商品价格
        shop_price = response.meta['shop_price']
        # 商品名称
        shop_title = response.xpath("normalize-space(//div[@class='name']/h2/text())").extract_first()
        # 产品品类
        shop_category_1 = response.xpath("normalize-space(//div[@class='p_r']/dl[1]/dd[1]/a[1]/text())").extract_first()
        shop_category_2 = response.xpath("normalize-space(//div[@class='p_r']/dl[1]/dd[1]/a[2]/text())").extract_first()
        # 商品品牌
        shop_brand = response.xpath("normalize-space(//div[@class='p_r']/dl[1]/dd[2]/a[1]/text())").extract_first()
        # 适合肤质
        shop_fuzhi = response.xpath("normalize-space(//div[@class='p_r']/dl[3]/dd/text())").extract_first()
        # 多少人想用
        shop_like = response.xpath("normalize-space(//div[@class='p_r_b']/a[1]/span[1]/text())").extract_first()
        # 多少人爱用
        shop_love = response.xpath("normalize-space(//div[@class='p_r_b']/a[2]/span[1]/text())").extract_first()
        # 多少评论
        shop_comment_amount = response.xpath(
            "normalize-space(//div[@class='p_r_b']/a[3]/span[1]/text())").extract_first()
        # 评论内容
        shop_comment_list = response.xpath("//div[@class='txt']/a/text()").extract()
        shop_comment = ','.join(shop_comment_list)
        item['shop_price'] = shop_price
        item['shop_title'] = shop_title
        item['shop_category_1'] = shop_category_1
        item['shop_category_2'] = shop_category_2
        item['shop_brand'] = shop_brand
        item['shop_fuzhi'] = shop_fuzhi
        item['shop_like'] = shop_like
        item['shop_love'] = shop_love
        item['shop_comment_amount'] = shop_comment_amount
        item['shop_comment'] = shop_comment
        print(item)
        yield item
