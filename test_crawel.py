#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""
@File: test_crawl_all.py
@Time: 2018/5/15 17:50
@Author:lei.tang@tongfudun.com
@Funtion:unittest for crawl_all api
"""

import time
import os
import logging

import re
from selenium import webdriver
from pymongo import MongoClient
from conf.settings import MONGODB
from core.crawler.config import PARAMS
from core.core_api import *
import requests
import urllib3
from selenium.webdriver.chrome.options import Options
from TestCase.test_common import *

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='logs/monogo.log',
                    filemode='a'
                    )




# Run crawl_all function
class TestCrawlAll:

    def __init__(self, params=None):
        self.craw = crawl_all(params)
        logging.info("The crawl_all is completed.")


# Run clean_wash function
class TestCleanWash:

    def __init__(self):
        self.clean = clean_wash()
        logging.info("The clean_wash is completed.")


# Run the word crawl in Baidu
# class TestBaiduSpider:
#
#     def __init__(self, word):
#         self.baidu = crawl_with_baidu(word)
#         logging.info("The baiduSpider is completed.")


# 判断爬虫后的url是否正确
class VerifyUrl:

    def __init__(self):
        pass

    def read_url(self, url):
        # requests.packages.urllib3.disable_warnings()
        # http = urllib3.PoolManager()
        # req = http.request("GET", url, headers=header)
        # return req

        # chrome_options=Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        driver = webdriver.PhantomJS()
        # driver.set_window_size(800, 600)
        driver.get(url)
        # time.sleep(2)
        title = driver.title
        driver.quit()
        return url, title





# Run crawl_one function
class TestCrawlOne:

    def __init__(self, url, screenshot=False):
        self.crawl_one = crawl_one(url, screenshot)
        logging.info("The crawl_one is completed.")


#读取wvs report的数据
class Report:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get(r"C:\Users\Administrator\Downloads\Developer.html")

    def reader(self):
        driver = self.driver
        elements = driver.find_elements_by_css_selector("font[color='green']")
        with open("logs/html.txt", 'w') as f:
            for i in elements:
                f.write("".join((i.text, "\n")))

        # file=driver.get_screenshot_as_png()
        #
        # with open("tco_1.png", "wb") as f2:
        #     f2.write(file)


    def __del__(self):
        self.driver.close()


if __name__ == "__main__":


    collection_tmp = 'crawler_urls_tmp'
    collection_clean = "crawler_urls"
    # url_crawl_one = "https://www.baidu.com"
    PARAMS['start_url'] = "http://m.dayspay.com.cn/daysmapp" # "https://www.lljr.com/about/lxwm"
    PARAMS['allowed_domains'] = []#m.daysluck.com:443
    # PARAMS['end_type'] = ''
    # PARAMS['start_url_request_method'] = "POST"
    # PARAMS['depth'] = 1
    # PARAMS['amount'] = 300
    # PARAMS['queue_size'] = 10
    # PARAMS['exclude_keywords'] = ["jquery.min.js", "zeroModal.css"]
    # PARAMS['cookies'] = {"jsessionid":"8E71D5E66AA9DAA7227390FF258137C"}
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))


    # # run crawl_all api testing
    # tca = TestCrawlAll(PARAMS)
    # # query the monoga db for all urls
    # connMon_tmp = ConnectMonGoQA()
    # connMon_tmp.save_data(collection_tmp, "logs/tmp.txt", "logs/origin_tmp.txt",type='url')


    # # run clean_wash api testing
    # tcw = TestCleanWash()
    # # query the monoga db for clean urls
    # connMon_clean = ConnectMonGoQA()
    # connMon_clean.save_data(collection_clean, "logs/clean.txt", "logs/origin_clean.txt",type='url')

    # #Query the wvs report
    # report = Report()
    # report.reader()

    # # run CrawlOne api testing
    # tco_false = TestCrawlOne(url_crawl_one)
    # with open("logs/tco.txt", "w", encoding="utf-8") as f:
    #     for k, v in tco_false.crawl_one.items():
    #         f.write("".join(("{0}:{1}".format(k, v), "\n")))
    #
    # tco_true = TestCrawlOne(url_crawl_one, screenshot=True)
    # with open("logs/tco_1.jpg", "wb") as f:
    #     for k, v in tco_true.crawl_one.items():
    #         if k == "screen_image":
    #             print(v)
    #             f.write(v)

    # with open("tco_1.txt", "w", encoding="utf-8") as f1:
    #         # , open("tco_1.png", "wb") as f2:
    #     for k, v in tco_true.crawl_one.items():
    #         # if k== "screenshot":
    #         #     f2.write(v)
    #         f1.write("".join(("{0}:{1}".format(k, v), "\n")))

    #loop the crawel
    #
    # for i in range(20):
    tca = TestCrawlAll(PARAMS)
    connMon_tmp = ConnectMonGoQA()
    tcw = TestCleanWash()
    connMon_clean = ConnectMonGoQA()

    # connMon_clean.remove(collection_clean,{'url':'https://www.lljr.com:443/css/style.css?v=20180604'})
    # connMon_clean.remove(collection_clean,{'url':'https://www.lljr.com:443/css/common.css?v=20180604'})

    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))