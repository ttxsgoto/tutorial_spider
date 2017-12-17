#!/usr/bin/env python
# coding: utf-8
from urllib import parse
import scrapy
from tutorial_spider.items import HuxiuItem, TakeFirstItemLoader


class HuxiuSpider(scrapy.Spider):
    name = "huxiu"
    allowed_domains = ["huxiu.com"]
    start_urls = [
        "http://www.huxiu.com/index.php"
    ]

    custom_settings = {
        "ITEM_PIPELINES": {
            'tutorial_spider.pipelines.HuxiuMyslqchemyPipeline': 20,
        },
    }

    def parse(self, response):
        url_path = response.css('.mod-info-flow .mob-ctt')
        for i in url_path:
            url = i.css('a::attr(href)').extract_first()
            desc = i.css('.mob-sub::text').extract_first()
            url = parse.urljoin(response.url, url)
            yield scrapy.Request(url,
                                 meta={'desc': desc},
                                 callback=self.parse_article)

    def parse_article(self, response):
        detail = response.css('div .article-wrap')
        item_loader = TakeFirstItemLoader(item=HuxiuItem(), selector=detail)
        item_loader.add_value('desc', response.meta.get('desc', ''))
        item_loader.add_css('title', '.t-h1::text')
        item_loader.add_value('link', response.url)
        item_loader.add_css('published', '.article-time::text')
        item = item_loader.load_item()
        yield item

