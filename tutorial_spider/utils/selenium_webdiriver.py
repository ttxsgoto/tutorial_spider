#!/usr/bin/env python
# coding: utf-8
"""
Describe:
https://selenium-python-zh.readthedocs.io/en/latest/index.html
"""

import time
import unittest

from selenium import webdriver  # selenium.webdriver 模块提供了所有WebDriver的实现,如Firefox, Chrome, IE and Remote
from selenium.webdriver.common.keys import Keys # `Keys`类提供键盘按键的支持


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()     # 创建实例

    def test_search(self):
        driver = self.driver
        driver.get("http://www.python.org") # 方法将打开URL中填写的地址，WebDriver 将等待， 直到页面完全加载完毕（其实是等到”onload” 方法执行完毕），然后返回继续执行你的脚本。 值得注意的是，如果你的页面使用了大量的Ajax加载， WebDriver可能不知道什么时候页面已经完全加载
        self.assertIn("Python", driver.title)     # driver.title 表示网页标题
        self.assertEqual()
        elem = driver.find_element_by_name("q")
        elem.clear()    # 预先清除input输入框中的任何预填充的文本
        elem.send_keys("pycon") # 输入搜索字
        elem.send_keys(Keys.RETURN) # 发送keys，这个和使用键盘输入keys类似。 特殊的按键可以通过引入`selenium.webdriver.common.keys`的 Keys 类来输入,如enturn,
        time.sleep(10)
        assert "No results found." not in driver.page_source    # driver.page_source 网页html源文件

    def tearDown(self):
        self.driver.close() # close只会关闭一个标签页; quit关闭整个浏览器


# if __name__ == "__main__":
#     unittest.main()

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# driver = webdriver.Chrome()
# driver.get("https://www.baidu.com/")
# driver.implicitly_wait(10) # seconds
# myDynamicElement = driver.find_element_by_id("s_btn_wr")

# print(myDynamicElement)
# try:
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "s_btn_wr"))
#     )
# finally:
#     driver.quit()

browser = webdriver.Chrome()
browser.get("http://www.python.org")

elem = browser.find_element_by_css_selector('input#id-search-field')
elem.clear()
elem.send_keys('python')
browser.find_element_by_css_selector('button#submit').click()
# 将得到的网页通过scrapy的Selector来解析
from scrapy.selector import Selector
selector = Selector(text=browser.page_source)
submit = selector.css('button#submit::text').extract_first()
print(submit)

