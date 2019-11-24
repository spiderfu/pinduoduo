# -*- coding: utf-8 -*-
"""
@Time : 2019/11/19 12:02
@Author : Spider fu
@File : pinduoduo_url.py
"""
import scrapy
import re
import MySQLdb
import MySQLdb.cursors
import bs4
import xlwt
import time
from EducationSpider.items import Caigou_zhongbiao_Item
from selenium import webdriver
from scrapy.selector import Selector
from selenium.webdriver.chrome.options import Options
chrome_option = Options()
chrome_option.add_argument("--disable-extensions")
chrome_option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

browser = webdriver.Chrome(executable_path="D:/chromedriver/chromedriver_win32/chromedriver.exe",
                           chrome_options=chrome_option)
url="https://youhui.pinduoduo.com/search/landing?keyword=%E7%A7%AD%E5%BD%92%E8%84%90%E6%A9%99"
# browser = webdriver.Chrome(executable_path="D:/chromedriver/chromedriver_win32/chromedriver.exe", chrome_option=chrome_option)
browser.get(url)
import time
time.sleep(1)
id=0
j_selector = Selector(text=browser.page_source)
len1=len(j_selector.xpath("//*[@id='__next']/div/div[2]/div/div[2]/a").extract())
url1="https://youhui.pinduoduo.com"
for i in range(1,61):
    n=j_selector.xpath("//*[@id='__next']/div/div[2]/div/div[2]/a["+str(i)+"]/@href").extract()[0]

    detail_url=str(url1)+str(n)
    print(detail_url)
    id=id+1
    insert_sql = """
                                   INSERT INTO pinduoduo(id,网址) 
                                   VALUES (%s,%s)
                                           """
    conn2 = MySQLdb.connect('127.0.0.1', 'root', 'fuzizhu', 'education_db', charset="utf8", use_unicode=True)
    cur2 = conn2.cursor()
    cur2.execute(insert_sql, (id,detail_url))
    conn2.commit()
for i in range(24):
    browser.find_element_by_xpath("//*[@id='__next']/div/div[2]/div/div[3]/div[2]/div[2]/a[1]").click()
    len1 = len(j_selector.xpath("//*[@id='__next']/div/div[2]/div/div[2]/a").extract())
    for i in range(1,(len1+1)):
        n=j_selector.xpath("//*[@id='__next']/div/div[2]/div/div[2]/a["+str(i)+"]/@href").extract()[0]

        detail_url=str(url1)+str(n)
        print(detail_url)
        id=id+1
        insert_sql = """
                                   INSERT INTO pinduoduo(id,网址) 
                                   VALUES (%s,%s)
                                               """
        conn2 = MySQLdb.connect('127.0.0.1', 'root', 'fuzizhu', 'education_db', charset="utf8", use_unicode=True)
        cur2 = conn2.cursor()
        cur2.execute(insert_sql, (id,detail_url))
        conn2.commit()
    print(len1)

