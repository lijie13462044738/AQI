# -*- coding: utf-8 -*-
import scrapy

from AQI.items import AqiItem



class ApiSpider(scrapy.Spider):
    name = 'api'
    allowed_domains = ['aqistudy.cn']
    base_url = 'https://www.aqistudy.cn/historydata/'
    start_urls = ["https://www.aqistudy.cn/historydata/"]

    # 1 解析第一层，每个城市的连接
    def parse(self, response):
        item = AqiItem()
        city_name_list = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/ul/div[2]/li/a/text()').extract()
        city_link_list = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/ul/div[2]/li/a/@href').extract()
        for city_name,city_link in zip(city_name_list,city_link_list):
            month_url = self.base_url + city_link
            item["city_name"] = city_name
            yield scrapy.Request(url=month_url,meta={"aqi_item":item}  ,callback=self.month_parse)

    # 2 解析城市每个月的连接
    def month_parse(self,response):

        # 取出iem
        item = response.meta["aqi_item"]
        month_list = response.xpath('/html/body/div[3]/div[1]/div[1]/table//tr/td/a/@href').extract()
        print "111111111111111111111111111111111111111111111111111111111",month_list
        for day_link in month_list:
            day_url = self.base_url + day_link
            yield scrapy.Request(url=day_url,meta={"aqi_item":item},callback=self.day_parse)

    # 3 获取城市每天的空气质量数据
    def day_parse(self,response):
        item = response.meta["aqi_item"]
        tr_list = response.xpath('//tr')
        tr_list.pop(0)
        for data in tr_list:

            item['date'] = data.xpath('./td[1]/text()').extract_first()
            item['AQI'] = data.xpath('./td[2]/text()').extract_first()
            item['level'] = data.xpath('./td[3]/span/text()').extract_first()
            item['pm2_5'] = data.xpath('./td[4]/text()').extract_first()
            item['pm10'] = data.xpath('./td[5]/text()').extract_first()
            item['so_2'] = data.xpath('./td[6]/text()').extract_first()
            item['co'] = data.xpath('./td[7]/text()').extract_first()
            item['no_2'] = data.xpath('./td[8]/text()').extract_first()
            item['o3'] = data.xpath('./td[9]/text()').extract_first()
            yield item






