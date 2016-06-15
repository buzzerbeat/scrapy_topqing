import scrapy
import logging 

from tutorial.items import Topqing, TopqingImg 

class TopqingSpider(scrapy.Spider):
    name = "topqing"
    allowed_domains = ["topqing.com"]
    start_urls = [
        "http://www.topqing.com"
    ]
    items = {}

    def parse(self, response):
        filename = './test.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        for sel in response.xpath('//ul[contains(@class, "gallery-list")]/li'):
            item = Topqing()
            item['link'] = sel.xpath('a/@href').extract_first()
            item['title'] = sel.xpath('a/div/text()').extract_first()
            item['time'] = sel.xpath('div/text()').extract_first()
            if item['link'] is not None:
                item['imgs'] = [];
                yield scrapy.Request(item['link'], callback=self.parse_dir_contents, meta={'item':item});
                #items.append(item)

        #return items
    def parse_dir_contents(self, response):
        item = response.request.meta["item"]
        for sel in response.xpath('//ul[@id="lightgallery"]/li'):
            itemImg = TopqingImg()
            itemImg['img_link'] = sel.xpath('@data-src').extract_first()
            itemImg['title'] = sel.xpath('@title').extract_first()
            item['imgs'].append(itemImg)
        return item
