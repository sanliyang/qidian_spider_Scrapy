# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from csv import DictWriter
import os

import pymysql

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
class mysqlPipLine(object):
    conn = None
    cursor = None
    def open_spider(self,spider):
        self.conn = pymysql.Connect(host='127.0.0.1',
                                    port = 3306,
                                    user = 'root',
                                    password = '980325by',
                                    db = 'qidian')
    def process_item(self,item,spider):
        self.cursor = self.conn.cursor()
        if isinstance(item, BookItem):
            sql = f'insert into Book values {item["book_id"], item["book_name"], item["book_cover"], item["book_url"], item["author"], str(item["tags"]), item["summary"]}'
            print(sql)
            try:
                self.cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                print(e)
                self.conn.rollback()
        elif isinstance(item, SegItem):
            try:
                self.cursor.execute(f'insert into Seg values {item["seg_id"],item["title"],item["url"],item["book_id"]}')
                self.conn.commit()
            except Exception as e:
                print(e)
                self.conn.rollback()
        elif isinstance(item, SegDetailItem):
            try:
                self.cursor.execute(f'insert into SegDetail(seg_id, text) values {item["seg_id"],item["text"]}')
                self.conn.commit()
            except Exception as e:
                print(e)
                self.conn.rollback()
    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()