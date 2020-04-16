# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8
import time
import random
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .settings import KEYWORDS
from .models import JDXlx, db
# import pymysql
# from .settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_TABLE


class JDXiaoLongXiaSpider(object):
    """京东下龙虾全国店铺相关数据信息抓取"""
    def __init__(self):
        """初始化"""
        self.url = "https://www.jd.com/"
        self.driver_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"
        self.browser = webdriver.Chrome(executable_path=self.driver_path)
        self.wait = WebDriverWait(self.browser, 20)
        self.keywords = KEYWORDS
        self.count = 0

        # mysql数据库相关连接配置
        # self.db = pymysql.connect(
        #     host=MYSQL_HOST,
        #     port=MYSQL_PORT,
        #     user=MYSQL_USER,
        #     password=MYSQL_PASSWORD,
        #     database=MYSQL_DATABASE,
        #     charset="utf8"
        # )
        # self.cursor = self.db.cursor()
        # self.table = MYSQL_TABLE
        # self.__sql = None
        # self.keys = None
        # self.values = None

    def __str__(self):
        self.browser.close()

    def get_search_button(self):
        """
        获取搜索框和搜索按钮元素
        :return: 索框页面元素与搜索按钮页面元素组成的元组
        """
        # 获取搜索框页面元素
        search_element = self.wait.until(
            EC.presence_of_element_located((By.ID, "key"))
        )
        # 获取搜索按钮页面元素
        btn_element = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "button"))
        )
        # 以元祖的方式返回
        return search_element, btn_element

    def scroll_2(self):
        """将垂直滚动条下滑到页面最底部"""
        self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(random.uniform(3, 4))

    def get_page(self):
        """
        获取列表页源代码
        :return: response 列表页源代码
        """
        # 拖动滚动条到页面底部
        self.scroll_2()
        try:
            self.wait.until(
                EC.presence_of_all_elements_located((
                    By.XPATH, '//li[@class="gl-item"]//div[@class="p-img"]//img'
                ))
            )
        except TimeoutException:
            self.get_page()
        response = self.browser.page_source
        # 解析数据
        self.parse_page(response)

    def index_page(self):
        """
        获取列表页
        :return:
        """
        try:
            self.wait.until(
                EC.presence_of_all_elements_located((
                    By.XPATH, '//li[@class="gl-item"]//div[@class="p-img"]//img'
                ))
            )
        except TimeoutException:
            time.sleep(1)
            self.run()

        # 获取网页数据
        self.get_page()

        print("--------------->{}条数据<-------------".format(self.count))
        # 获取下一页按钮
        next_page_element = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "pn-next"))
        )
        if next_page_element:
            next_page_element.click()
            time.sleep(random.uniform(2, 3))
            self.index_page()

        # 退出程序
        self.browser.quit()

    def parse_page(self, response):
        """
        解析列表页，提取相关数据
        :param response: 列表页网页源代码
        :return:
        """
        html = etree.HTML(response)
        goods_li = html.xpath('//li[@class="gl-item"]')
        for good_li in goods_li:
            price = "".join(good_li.xpath('.//div[@class="p-price"]/strong//text()'))
            desc = "".join(good_li.xpath('.//div[@class="p-name p-name-type-2"]//em//text()'))
            comments = good_li.xpath('.//div[@class="p-commit"]/strong/a/text()')[0]
            shop = good_li.xpath('.//div[@class="p-shop"]//a/text()')
            shop = shop[0] if shop else ''
            goods_info = {
                "price": price,
                "desc": desc,
                "comments": comments,
                "shop": shop
            }
            self.count += 1
            # 将数据写入Mysql数据库
            print(goods_info)
            self.save_2_mysql(goods_info)

    @staticmethod
    def save_2_mysql(goods_info):
        """
        将数据写入mysql数据库
        :param goods_info: 一个商品相关数据 字典格式
        :return:
        """
        # self.keys = ", ".join(goods_info.keys())
        # self.values = ", ".join(["%s"]*len(goods_info))
        # try:
        #     self.cursor.execute(self.sql, tuple(goods_info.values()))
        #     self.db.commit()
        #     print("{}...数据成功写入数据库！".format(goods_info["shop"]))
        # except Exception as e:
        #     print(e.args)
        #     self.db.rollback()
        data = JDXlx(**goods_info)
        db.session.add(data)
        db.session.commit()
        print("{}...  数据成功写入数据库！".format(goods_info["shop"]))

    # @property
    # def sql(self):
    #     if not self.__sql:
    #         self.__sql = 'insert into %s(%s) values(%s)' % (self.table, self.keys, self.values)
    #     return self.__sql

    def run(self):
        """启动爬虫"""
        # 向京东网站发起请求
        self.browser.get(self.url)
        # 获取搜索框和搜索按钮元素
        search_element, btn_element = self.get_search_button()
        search_element.clear()
        search_element.send_keys(self.keywords)
        btn_element.click()

        # 获取列表页
        self.index_page()


if __name__ == '__main__':
    spider = JDXiaoLongXiaSpider()
    spider.run()


