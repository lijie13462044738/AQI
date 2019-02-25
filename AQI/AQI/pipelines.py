# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from datetime import datetime
# 1 数据源管道
import pymongo
import redis as redis
from scrapy.exporters import CsvItemExporter

# 1 数据源管道
class AqidataPipeline(object):
    def process_item(self, item, spider):
        item["data_source"] = spider.name
        item["date_time"] = str(datetime.utcnow())
        return item


# 2 保存json数据管道
class AqiPipeline(object):
    def open_spider(self,spider):
        self.file = open("api.json", "w")

    def process_item(self, item, spider):
        data = json.dumps(dict(item)) + "\n"
        self.file.write(data)
        return item

    def close_spider(self,spider):
        self.file.close()

# 3 保存csv数据管道
class CsvPipeline(object):
    def open_spider(self,spider):
        self.file = open("api.csv", "w")
        # 创建一个读写器
        self.writer = CsvItemExporter(self.file)
        # 开启读写器
        self.writer.start_exporting()

    def process_item(self, item, spider):
        self.writer.export_item(item)
        return item

    def close_spider(self,spider):
        self.file.close()
        self.writer.finish_exporting()

# 4 保存到mongodb数据库
class MongodbPipeline(object):

    def open_spider(self,spider):

        # 创建一个mongodb连接
        self.client = pymongo.MongoClient("127.0.0.1", 6379)
        # 创建一个数据库
        self.db = self.client.AQI_mongo
        #创建一个集合
        self.collections = self.db.aqi

    def process_item(self,item,spider):
        # 写入数据
        self.collections.insert(dict(item))
        return item

    def  close_spider(self,spider):
        # 关闭连接
        self.client.close()


class RedisPipeline(object):

    def open_spider(self,spider):
        self.client = redis.Redis('127.0.0.1', 6379)

    def process_item(self, item, spider):
        self.client.lpush('AQI_LIST', dict(item))
        return item
