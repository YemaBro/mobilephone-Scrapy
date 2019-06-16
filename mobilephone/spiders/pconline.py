# -*- coding: utf-8 -*-
import scrapy
from mobilephone.items import PconlineNewsTest


class MobilphoneSpider(scrapy.Spider):
    name = 'pconline'
    allowed_domains = ['mobile.pconline.com.cn']
    start_urls = ['https://mobile.pconline.com.cn/dclub/']

    def parse(self, response):
        news = response.css('.list-wrap li')
        for new in news:
            item = PconlineNewsTest()
            item['url'] = new.css('a::attr(href)').extract_first().lstrip('/')
            item['title'] = new.css('dt::text').extract_first()
            item['author'] = new.css('dd i.author::text').extract_first()
            item['date'] = new.css('dd i.time::text').extract_first()
            item['tags'] = new.css('.keyword a::text').extract()
            yield item

        nexturl = response.css('#page a:last-child::attr(href)').extract_first()
        if nexturl is not None:
            full_url = 'https://' + nexturl
            yield scrapy.Request(url=full_url, callback=self.parse, dont_filter=False)

