# -*- coding: utf-8 -*-
import datetime
from urllib import parse
import scrapy
import logging

from tutorial_spider.items import TakeFirstItemLoader, TtxsgotoItem
logger = logging.getLogger(__name__)


class Ttxsgoto01Spider(scrapy.Spider):
    name = 'ttxsgoto01'
    allowed_domains = ['ttxsgoto.github.io']
    start_urls = ['http://ttxsgoto.github.io/']

    custom_settings = {
        "ITEM_PIPELINES": {
            'tutorial_spider.pipelines.TtxsgotoFilterPipeline': 10,
            'tutorial_spider.pipelines.TtxsgotoBlogMysqlchemyPipeline': 20,
        },
    }

    def parse(self, response):
        articles = response.css('#main .post')
        for article in articles:
            article_url = article.css('h1 a::attr(href)').extract_first()
            url = parse.urljoin(response.url, article_url)
            yield scrapy.Request(url, callback=self.parse_article)

        next_url = response.css('#page-nav a[rel="next"][href]').css('::attr(href)').extract_first()
        if next_url:
            yield scrapy.Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_article(self, response):
        """解析文章详情"""
        item_loader = TakeFirstItemLoader(item=TtxsgotoItem(), selector=response)
        item_loader.add_css('title', '#main header a::text')
        item_loader.add_value('url', response.url)
        item_loader.add_css('publish', '.article-time time::text')
        item_loader.add_css('content', '.article-content')
        item_loader.add_css('classify', '.article-tags a::text')
        item_loader.add_css('lable', '.article-categories a::text')
        item_loader.add_value('create_time', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        item = item_loader.load_item()
        yield item