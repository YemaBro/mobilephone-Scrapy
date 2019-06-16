# -*- coding: utf-8 -*-
import scrapy
from mobilephone.items import CnmoNewsTest


class CnmoSpider(scrapy.Spider):
    name = 'cnmo'
    allowed_domains = ['www.cnmo.com']
    base_url = 'http://www.cnmo.com/phone/news/{page}/'

    def start_requests(self):
        for page in range(1, 81):
            url = self.base_url.format(page=page)
            yield scrapy.Request(url=url, callback=self.parse_info, dont_filter=True)

    def parse_info(self, response):
        news = response.css('.listbox .libox .txtbox')
        for new in news:
            item = CnmoNewsTest()
            item['url'] = new.css("a::attr(href)").extract_first()
            item['title'] = new.css("a h2::text").extract_first()
            item['tags'] = new.css(".botbox ul li span a::text").extract()
            for i in range(len(item['tags'])):
                item['tags'][i] = item['tags'][i].strip()
            yield scrapy.Request(url=item['url'], callback=self.parse_detail, meta={'item': item}, dont_filter=True)

    def parse_detail(self, response):
        item = response.meta.get('item')
        details = response.xpath("//div[@class='ctitle']/div[@class='ctitle_spe']/div[@class='fl']")
        for detail in details:
            item['author'] = detail.xpath("span[@class='text_auther']/text()").get()
            item['date'] = detail.xpath("span[3]/text()").get()
            yield item