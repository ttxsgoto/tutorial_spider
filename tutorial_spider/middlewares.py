# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

from scrapy import signals
from tutorial_spider.settings import  USER_AGENT_LIST
from fake_useragent import UserAgent


class TutorialSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class AutoRandomUserAgentMiddlware(object):
    """随机更换user-agent"""

    def __init__(self, crawler):
        super(AutoRandomUserAgentMiddlware, self).__init__()
        self.ua = UserAgent()
        # 读取在settings文件中的配置，来决定ua采用哪个方法，默认是random，也可是ie、Firefox等等，参考前面的使用方法。
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    # 更换用户代理逻辑在此方法中
    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        print(get_ua())
        request.headers.setdefault('User-Agent', get_ua())


class RandomUserAgentMiddleware(object):
    """
    在settings定义agent列表来随机选择user-agent
    """
    def process_request(self, request, spider):
        ua  = random.choice(USER_AGENT_LIST)
        agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:57.0) Gecko/20100101 Firefox/57.0"
        if ua:
            request.headers.setdefault('User-Agent', ua)
        else:
            request.headers.setdefault('User-Agent', agent)


from selenium import webdriver
from scrapy.http import HtmlResponse
class JSPageMiddleware(object):
    #通过chrome请求动态网页
    def process_request(self, request, spider):
        if spider.name == "ttxsgoto02":
            browser = webdriver.Chrome()
            browser.get(request.url)
            return HtmlResponse(url=browser.current_url, body=browser.page_source, encoding="utf-8", request=request)
