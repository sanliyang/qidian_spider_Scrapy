# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    book_id = scrapy.Field()
    book_name = scrapy.Field()
    book_cover = scrapy.Field()
    book_url = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    summary = scrapy.Field()

class SegItem(scrapy.Item):
    book_id = scrapy.Field()
    seg_id = scrapy.Field()   # 章节id
    title = scrapy.Field()
    url = scrapy.Field()

class SegDetailItem(scrapy.Item):
    seg_id = scrapy.Field()    # 章节ID
    text = scrapy.Field()      # 内容