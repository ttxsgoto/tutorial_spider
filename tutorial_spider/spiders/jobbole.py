# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from urllib import parse
from tutorial_spider.items import JobBoleArticleItem, TakeFirstItemLoader
from tutorial_spider.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    # custom_settings = {
    #     "ITEM_PIPELINES": {
    #         'tutorial_spider.pipelines.Movietop250Pipeline': 1,
    #         # 'tutorial_spider.pipelines.Movietop250JsonPipeline': 10,
    #         # 'tutorial_spider.pipelines.Movietop250MysqlAsynPipeline': 20,
    #         'tutorial_spider.pipelines.Movietop250MongdbPipeline': 20,
    #         'tutorial_spider.pipelines.Movietop250MyslqchemyPipeline': 25,
    #     },
    #     "IMAGES_URLS_FIELD": 'img_url'
    # }

    def parse(self, response):
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first('')
            post_url = post_node.css("::attr(href)").extract_first('')
            yield Request(url=parse.urljoin(response.url, post_url), meta={'front_image_url':image_url}, callback=self.parse_detail)

        next_url = response.css('.next.page-numbers ::attr(herf)').extract_first('')
        if next_url:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)

    def parse_detail(self, response):
        """
        提取文章中的具体字段
        :param response:
        :return:
        """
        # article_item = JobBoleArticleItem()
        # 文章封面图url地址
        # front_image_url = response.meta.get('front_image_url', '')
        # xpath 选择器, extract_first: 选择第一个值,如果没有就设置为default
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first(default='')
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace('·', '').strip()
        # 点赞数,  class中包含某种属性
        # praise_nums = int(response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0])
        # fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
        # match_re = re.match(".*(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        # comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        # match_re = re.match(".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        # content = response.xpath("//div[@class='entry']").extract()[0]
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [el for el in tag_list if not el.strip().endswith("评论")]
        # tags = ','.join(tag_list)

        # css选择器
        # title = response.css(".entry-header h1::text").extract()[0]
        # create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace('·','').strip()
        # praise_nums = int(response.css('.vote-post-up h10::text').extract()[0])
        # fav_nums = response.css('span.bookmark-btn::text').extract()[0]
        # match_re = re.match(".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0

        # comment_nums = response.css('a[href="#article-comment"] span::text').extract()[0]
        # match_re = re.match(".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        #
        # content = response.css('div.entry').extract()[0]
        # tag_list = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        # tag_list = [el for el in tag_list if not el.strip().endswith("评论")]
        # tags = ','.join(tag_list)
        # article_item['title'] = title
        # article_item['url'] = response.url
        # try:
        #     create_date = datetime.datetime.strptime(create_date,"%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # article_item['create_date'] = create_date
        # article_item['front_image_url'] = [front_image_url]
        # article_item['praise_nums'] = praise_nums
        # article_item['comment_nums'] = comment_nums
        # article_item['fav_nums'] = fav_nums
        # article_item['tags'] = tags
        # article_item['content'] = content
        # article_item['url_object_id'] = get_md5(response.url)

        # 文章封面图url地址
        front_image_url = response.meta.get('front_image_url', '')
        item_loader = TakeFirstItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css('title', ".entry-header h1::text")
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_css('create_date', 'p.entry-meta-hide-on-mobile::text')
        item_loader.add_value('front_image_url', [front_image_url])
        item_loader.add_css('praise_nums', '.vote-post-up h10::text')
        item_loader.add_css('comment_nums', 'a[href="#article-comment"] span::text')
        item_loader.add_css('fav_nums', 'span.bookmark-btn::text')
        item_loader.add_css('tags', 'p.entry-meta-hide-on-mobile a::text')
        item_loader.add_css('content', 'div.entry')
        # 将item_loader进行解析对象处理, 1.将所有值转换成list 需要转化, 2.对部分值需要添加处理函数进行处理操作
        article_item = item_loader.load_item()

        yield article_item
