# -*- coding: utf-8 -*-
"""
@Time : 2019/11/22 12:02
@Author : Spider fu
@File : pinduoduo_comment.py
"""
import MySQLdb.cursors
import bs4
import time
from selenium import webdriver
from scrapy.selector import Selector
from selenium.webdriver.chrome.options import Options
chrome_option = Options()
chrome_option.add_argument("--disable-extensions")
chrome_option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
browser = webdriver.Chrome(executable_path="D:/chromedriver/chromedriver_win32/chromedriver.exe", chrome_options = chrome_option)
browser.get("http://mobile.yangkeduo.com/search_result.html?search_key=%E7%A7%AD%E5%BD%92%E8%84%90%E6%A9%99&search_src=new&search_met=btn_sort&search_met_track=manual&refer_page_name=search&refer_page_id=10031_1574404010595_tKgcVwJ985&refer_page_sn=10031&page_id=10015_1574404019895_1frD3dDZAf&list_id=zEBDtYIKiC&flip=20%3B0%3B0%3B0%3B65ced1b3-e180-4ff9-b51f-55b8e4909754&sort_type=_sales&price_index=-1&filter=")
error = 0
for m in range(1,200):
    print(m)
    for q in range(32):
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(0.1)
    j_selector = Selector(text=browser.page_source)
    title = j_selector.css("#main > div > div:nth-child(2) > div > div._3gvC_QPr > div._1TRchgB6 > div > div:nth-child("+str(m)+") > div > div._1SZEO9z8 > div.pHbSR-xp._1cP_KihG::text").extract()[0]
    # title = "【买5送5斤】秭归脐橙当季新鲜孕妇水果高山手剥橙子3/5/10斤"
    browser.find_element_by_css_selector("#main > div > div:nth-child(2) > div > div._3gvC_QPr > div._1TRchgB6 > div > div:nth-child("+str(m)+") > div > div.u1hv-9Ep > div").click()
    time.sleep(1)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(0.1)
    browser.find_element_by_css_selector("#main > div > div._3fjhuw0e > div._1AwsJ8JQ > div ").click()
    # for j in range(25):
    #     browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    #     time.sleep(1)
    # list = len(j_selector.xpath("//*[@id='goods-comments-list']/div/div/div/div").extract())
    for i in range(1,251):
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(0.5)
        j_selector = Selector(text=browser.page_source)
        text = j_selector.xpath("//*[@id='goods-comments-list']/div/div/div/div["+str(i)+"]/div[2]/span/text()").extract()[0]
        guige = j_selector.css("#goods-comments-list > div > div > div.pdd-list-container > div:nth-child("+str(i)+") > div.gc-spec > span:nth-child(1)::text").extract()[0]
        try:
            browser.find_element_by_css_selector("#goods-comments-list > div > div > div > div:nth-child("+str(i)+") > div.gc-spec > span.see-more").click()
            # goods-comments-list > div > div > div.pdd-list-container > div:nth-child(37) > div.gc-spec > span.see-more
        except:
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(0.1)
            # error = error + 1
            # print(error)
            # continue
            browser.find_element_by_css_selector("#goods-comments-list > div > div > div.pdd-list-container > div:nth-child("+str(i)+") > div.gc-spec > span.see-more").click()
        finally:
            html_doc = browser.page_source
            soup = bs4.BeautifulSoup(html_doc, 'lxml')
            test_xiangxi = soup.find(name="div", attrs={"class": "_2LhYUXJk"})
            comment_time = test_xiangxi.get_text()
            browser.find_element_by_css_selector("#main > div.goods-comments-container.container > div.y9Zon0X3 > div > div._33bmGLnO").click()
            insert_sql = """
                                                      INSERT INTO pinduoduo_comment(标题,规格,评论,时间) 
                                                      VALUES (%s,%s,%s,%s)
                                                                  """
            conn2 = MySQLdb.connect('127.0.0.1', 'root', 'fuzizhu', 'education_db', charset="utf8mb4", use_unicode=True)
            cur2 = conn2.cursor()
            cur2.execute(insert_sql, (title,guige,text,comment_time))
            conn2.commit()
            print(text,title,guige,comment_time)
            time.sleep(0.1)
    browser.get(
        "http://mobile.yangkeduo.com/search_result.html?search_key=%E7%A7%AD%E5%BD%92%E8%84%90%E6%A9%99&search_src=new&search_met=btn_sort&search_met_track=manual&refer_page_name=search&refer_page_id=10031_1574404010595_tKgcVwJ985&refer_page_sn=10031&page_id=10015_1574404019895_1frD3dDZAf&list_id=zEBDtYIKiC&flip=20%3B0%3B0%3B0%3B65ced1b3-e180-4ff9-b51f-55b8e4909754&sort_type=_sales&price_index=-1&filter=")

