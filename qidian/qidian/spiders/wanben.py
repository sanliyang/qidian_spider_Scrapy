import uuid

import scrapy
from scrapy.http import Response, HtmlResponse, Request
from scrapy.selector import SelectorList, Selector

from qidian.items import *


class WanbenSpider(scrapy.Spider):
    name = 'wanben'
    allowed_domains = ['qidian.com']
    start_urls = ['https://www.qidian.com/finish']

    def parse(self, response):
       if response.status == 200:
           # 响应成功，解析数据
           lis = response.css('.all-img-list li')  # SelectorList
           for li in lis:
               item = BookItem()
               item['book_id'] = uuid.uuid4().hex

               # li 对象类型是Selector
               a = li.xpath('./div[1]/a')
               item["book_url"] = a.xpath('./@href').get()
               item["book_cover"] = a.xpath('./img/@src').get()
               item["book_name"] = li.xpath('./div[2]/h4/a/text()').get()
               item["author"], *item["tags"] = li.css('.author a::text').extract()
               item["summary"] = li.css('.intro::text').get()

               # 请求小说的详情
               yield Request('https://' + item['book_url'] + '#Catalog',
                             callback=self.parse_info, priority=10,
                             meta={'book_id': item['book_id']})

               yield item

           # 获取下一页链接
           next_url = 'https:' + response.css('.lbf-pagination-item-list').xpath('./li[last()]/a/@href').get()
           if next_url.find('javascript:;') == -1:   # 存在下一页
               yield Request(next_url, priority=100)

    def parse_info(self,response:Response):
        book_id = response.meta['book_id']
        seg_as = response.css('.volume li>a')
        for a in seg_as:
            # a-> Selector
            item = SegItem()
            item['seg_id'] = uuid.uuid4().hex
            item['book_id'] = book_id
            item['url'] = 'https:' + a.css('::attr("href")').get()
            item['title'] = a.css('::text').get()

            yield item

            yield Request(item['url'], callback=self.parse_seg,
                          priority=2,
                          meta={'seg_id':item['seg_id']})

    def parse_seg(self,response):
        item = SegDetailItem()
        texts = response.css('.read-content p').extract()
        for text in texts:
            item['seg_id'] = response.meta['seg_id']
            item['text'] = text.replace('\u3000','').replace('<p>','').replace('</p>','')
            yield item