# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from csv import DictWriter
import os

from qidian.items import *

class QidianPipeline:
    def __init__(self):
        self.book_csv = 'books.csv'
        self.juan_csv = 'juan.csv'
        self.seg_csv = 'seg.csv'
        self.detail_csv = 'detail.csv'

    def save_csv(self, item, filename):
        has_header = os.path.exists(filename)
        with open(filename,'a') as f:
            write = DictWriter(f, fieldnames = item.keys())
            if not has_header:
                write.writeheader()
            write.writerow(item)

    def process_item(self, item, spider):
        if isinstance(item,BookItem):
           self.save_csv(item, self.book_csv)
        elif isinstance(item,SegItem):
            self.save_csv(item,self.seg_csv)
        elif isinstance(item, SegDetailItem):
            self.save_csv(item, self.detail_csv)
        return item
