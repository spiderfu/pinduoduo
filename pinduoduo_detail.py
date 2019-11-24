# -*- coding: utf-8 -*-
"""
@Time : 2019/11/19 14:59
@Author : Spider fu
@File : pinduoduo_detail.py
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
conn1 = MySQLdb.connect('127.0.0.1', 'root', 'fuzizhu', 'education_db', charset="utf8", use_unicode=True)
cur1 = conn1.cursor()
cur1.execute("SELECT * FROM pinduoduo ")
result1 = cur1.fetchall()
flag = 0
for url in result1:
    print(url[1])
    print(url[0])
    detail_url = url[1]
    if url[0] == 256:
        flag = 1
    if flag == 1:
        try:
            chrome_option = Options()
            chrome_option.add_argument("--disable-extensions")
            chrome_option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

            browser = webdriver.Chrome(executable_path="D:/chromedriver/chromedriver_win32/chromedriver.exe",
                                       chrome_options=chrome_option)
            browser.get(detail_url)
            time.sleep(0.1)
            j_selector = Selector(text=browser.page_source)
            title=j_selector.xpath("//*[@id='__next']/div/div[2]/div/div[1]/div[2]/div[1]/text()").extract()[0]
            store=j_selector.xpath("//*[@id='__next']/div/div[2]/div/div[2]/div[1]/div[1]/text()").extract()[0]
            before_price=j_selector.xpath("//*[@id='__next']/div/div[2]/div/div[1]/div[2]/div[2]/p[1]/span[2]/text()[2]").extract()[0]
            after_price=j_selector.xpath("//*[@id='__next']/div/div[2]/div/div[1]/div[2]/div[2]/p[2]/span[2]/text()[2]").extract()[0]
            sales=j_selector.xpath("//*[@id='__next']/div/div[2]/div/div[1]/div[2]/div[2]/p[3]/text()").extract()[0]
            product_details=j_selector.xpath("//*[@id='__next']/div/div[2]/div/div[2]/div[2]/div[2]/div/text()").extract()[0]
            print(title,store,before_price,after_price,sales,product_details)
            insert_sql = """
                                           INSERT INTO product(网址,标题,店铺名称,原价,券后价,销量,商品详情)
                                           VALUES (%s,%s,%s,%s,%s,%s,%s)
                                                   """
            conn2 = MySQLdb.connect('127.0.0.1', 'root', 'fuzizhu', 'education_db', charset="utf8", use_unicode=True)
            cur2 = conn2.cursor()
            cur2.execute(insert_sql, (detail_url,title,store,before_price,after_price,sales,product_details))
            conn2.commit()
        except Exception as a:
            n=str(a)
            inset_sql = """
                                                                      INSERT INTO errors_2019(网址,异常)
                                                                      VALUES (%s,%s)
                                                                      """
            conn4 = MySQLdb.connect('127.0.0.1', 'root', 'fuzizhu', 'education_db', charset="utf8", use_unicode=True)
            cur4 = conn4.cursor()
            cur4.execute(inset_sql, (detail_url, str(a)))
            conn4.commit()

# for i in range(24):
#     browser.find_element_by_xpath("//*[@id='__next']/div/div[2]/div/div[3]/div[2]/div[2]/a[1]").click()
#     len1 = len(j_selector.xpath("//*[@id='__next']/div/div[2]/div/div[2]/a").extract())
#     for i in range(1,(len1+1)):
#         n=j_selector.xpath("//*[@id='__next']/div/div[2]/div/div[2]/a["+str(i)+"]/@href").extract()[0]
#
#         detail_url=str(url1)+str(n)
#         print(detail_url)
#         id=id+1
#         insert_sql = """
#                                    INSERT INTO pinduoduo(id,网址)
#                                    VALUES (%s,%s)
#                                                """
#         conn2 = MySQLdb.connect('127.0.0.1', 'root', 'fuzizhu', 'education_db', charset="utf8", use_unicode=True)
#         cur2 = conn2.cursor()
#         cur2.execute(insert_sql, (id,detail_url))
#         conn2.commit()
#     print(len1)
