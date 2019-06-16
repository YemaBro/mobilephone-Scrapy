# -*- coding: utf-8 -*-
import scrapy
import json
from mobilephone.items import ZolNewsTest


class ZolSpider(scrapy.Spider):
    name = 'zol'
    allowed_domains = ['www.zol.com.cn']
    base_url = 'http://dynamic.zol.com.cn/channel/index.php?c=Ajax_MobileData&a=MobileNews&cid=74&page='

    def start_requests(self):
        for page in range(0, 31):
            url = self.base_url + str(page)
            yield scrapy.Request(url=url, callback=self.parse_info, dont_filter=True)

    def parse_info(self, response):
        news = json.loads(response.text.strip('()')).get('data')
        for new in news:
            item = ZolNewsTest()
            item['title'] = new.get('title')
            item['url'] = new.get('url')
            yield scrapy.Request(url=item['url'], callback=self.parse_detail, dont_filter=True, meta={'item':item})

    def parse_detail(self, response):
        item = response.meta.get('item')
        details = response.xpath("//div[@class='article-aboute']")
        for detail in details:
            item['date'] = detail.xpath("span[@id='pubtime_baidu']/text()").get()
            item['author'] = detail.xpath("span[@id='author_baidu']/text()").get() + detail.xpath("span[@id='author_baidu']/a/text()").get()
            yield item