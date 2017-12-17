# -*- coding: utf-8 -*-
from urllib import parse
import scrapy
from tutorial_spider.items import Movietop250Item, DefaultItemLoader


class Douban250Spider(scrapy.Spider):
    name = 'douban_250'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250',]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    }

    # 该项目自定义的配置,如果这里配置过后,settings里面对应的配置就不生效,优先级更高
    custom_settings = {
        "ITEM_PIPELINES":{
            'tutorial_spider.pipelines.Movietop250Pipeline': 1,
            # 'tutorial_spider.pipelines.Movietop250JsonPipeline': 10,
            # 'tutorial_spider.pipelines.Movietop250MysqlAsynPipeline': 20,
            'tutorial_spider.pipelines.Movietop250MongdbPipeline': 20,
            'tutorial_spider.pipelines.Movietop250MyslqchemyPipeline': 25,
        },
        "IMAGES_URLS_FIELD": 'img_url'
    }


    def start_requests(self):
        return [scrapy.Request('https://movie.douban.com/top250', headers=self.headers)]

    def parse(self, response):
        nodes = response.css(".grid_view li")
        for node in nodes:
            # 使用itemloader解析
            item_loader = DefaultItemLoader(item=Movietop250Item(), selector=node)
            item_loader.add_css('num', 'em::text')
            item_loader.add_css('movie_detail_url', '.hd a::attr(href)')
            item_loader.add_css('img_url', 'a img::attr(src)')
            item_loader.add_css('name', '.hd .title::text')
            item_loader.add_css('grade', '.rating_num::text')
            item_loader.add_xpath('comment', '//*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[2]/div/span[4]/text()')
            item_loader.add_css('info', '.inq::text')
            item = item_loader.load_item()
            yield item
        next_url = response.css('.next a::attr(href)').extract_first()
        if next_url:
            yield scrapy.Request(url=parse.urljoin(response.url, next_url),headers=self.headers, callback=self.parse)


