# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time
import scrapy
from scrapy import signals
from selenium import webdriver
import time

class ChromeMiddleware(object):
    def process_request(self,request,spider):

        # 获取请求url
        url = request.url

        if url != "https://www.aqistudy.cn/historydata/":
            # 1 创建一个浏览器对象
            driver = webdriver.Chrome()

            # 2 发送请求
            driver.get(url)

            # 解决加载延迟的问题
            time.sleep(2)
            # 3 获取数据
            data = driver.page_source
            # print "&"*50,data
            # 4 关闭浏览器

            driver.quit()

            # 构建返回响应
            return scrapy.http.HtmlResponse(url=url,body=data.encode("utf-8"),encoding='utf-8', request=request)


