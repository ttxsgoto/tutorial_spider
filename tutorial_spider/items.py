# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import datetime
import re

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader

##########################################
# 公共方法
##########################################
from tutorial_spider.models import Movietop250, Huxiu, LagouPosition, ZhihuAnswer, ZhihuQuestion,\
    TtxsgotoBlog


class TakeFirstItemLoader(ItemLoader):
    """
    自定义item_loader, 修改为 默认取列表中的第一个值
    """
    default_output_processor = TakeFirst()


def remove_blank(value):
    """删除对应两边的空格"""
    return value.strip()


##########################################


def add_value(value):
    return value + '- goto'


def date_convert(value):
    try:
        create_date = str(datetime.datetime.strptime(value, "%Y/%m/%d").date())
    except Exception as e:
        create_date = str(datetime.datetime.now().date())
    return create_date


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def remove_comment_tags(value):
    """去掉tag中提取的评论"""
    # return value + 'test'
    if "评论" in value:
        return ''
    else:
        return value


def afer_comment_tags(value):
    return value + 'after'


def return_value(value):
    """解决图片url需要为可迭代对象问题"""
    return value


class ArticleItemLoader(ItemLoader):
    """
    自定义item_loader, 修改为 默认取列表中的第一个值
    """
    default_output_processor = TakeFirst()


######################################
# Jobbole
######################################


class JobBoleArticleItem(scrapy.Item):
    # input_processor 对传递过来的值进行预处理操作,通过相关的函数来处理值
    title = scrapy.Field(
        input_processor = MapCompose(lambda x: x + "- ttxs", add_value)
    )
    create_date = scrapy.Field(
        input_processor = MapCompose(date_convert),
        # output_processor = TakeFirst() # 返回第一个值
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor= MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor = MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=MapCompose(afer_comment_tags)
        # input_processor=MapCompose(remove_comment_tags),
        # output_processor = Join(',')
    )
    content = scrapy.Field()


######################################
# Movietop250
######################################


def get_value(value):
    """从字符串中取出数字"""
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        num = match_re.group()
    else:
        num = ''
    return num


class DefaultItemLoader(ItemLoader):
    """自定义itemloader添加默认的output添加第一个不为空数据"""
    default_output_processor = TakeFirst()


class Movietop250Item(scrapy.Item):
    num = scrapy.Field()
    movie_detail_url = scrapy.Field()
    img_url = scrapy.Field(
        output_processor=MapCompose(return_value,)
    )
    img_file_path = scrapy.Field()
    name = scrapy.Field()
    grade = scrapy.Field()
    comment = scrapy.Field(
        input_processor = MapCompose(get_value),
    )
    info = scrapy.Field()

    def insert_to_mysql(self):
        movie_detail_url=self["movie_detail_url"]
        item_sql = Movietop250(
            num=self["num"],
            movie_detail_url=movie_detail_url,
            img_url=self["img_url"][0],
            img_file_path=self["img_file_path"][0],
            name=self["name"].encode("utf-8"),
            grade=self["grade"],
            comment=self["comment"],
            info=self["info"].encode("utf-8"),
        )
        return item_sql


######################################
# Zhihu
######################################


class ZhihuQuestionItem(scrapy.Item):
    #知乎的问题 item
    zhihu_id = scrapy.Field(output_processor=TakeFirst(),)      # 知乎id
    topics = scrapy.Field(
        output_processor=TakeFirst(),
    )                                                           # 主题
    url = scrapy.Field(output_processor=TakeFirst(),)           # url
    title = scrapy.Field(output_processor=TakeFirst(),)         # 标题
    content = scrapy.Field(output_processor=TakeFirst(),)       # 内容
    answer_num = scrapy.Field(output_processor=TakeFirst(),)    # 回答数量
    comments_num = scrapy.Field(
        output_processor=MapCompose(remove_comment_tags),)       # 评论数量
    watch_user_num = scrapy.Field(output_processor=TakeFirst(),) # 关注者数量
    click_num = scrapy.Field(output_processor=TakeFirst(),)      # 浏览数量
    crawl_time = scrapy.Field(output_processor=TakeFirst(),)     # 爬取时间

    def insert_to_mysql(self):
        item_sql = ZhihuQuestion(
            zhihu_id=self["zhihu_id"],
            topics=self["topics"],
            url=self["url"],
            title=self["title"],
            content=self["content"],
            answer_num=self["answer_num"],
            comments_num=self["comments_num"],
            watch_user_num=self["watch_user_num"],
            click_num=self["click_num"],
            crawl_time=self["crawl_time"]
        )

        return item_sql


class ZhihuAnswerItem(scrapy.Item):
    #知乎的问题回答item

    zhihu_id = scrapy.Field()   # 知乎id
    url = scrapy.Field()        # url
    question_id = scrapy.Field()# 问题id
    author_id = scrapy.Field()  # 作者id
    content = scrapy.Field()    # 内容
    parise_num = scrapy.Field() #
    comments_num = scrapy.Field()# 评论数量
    create_time = scrapy.Field()# 创建时间
    update_time = scrapy.Field()# 更新时间
    crawl_time = scrapy.Field() # 爬取时间

    def insert_to_mysql(self):
        item_sql = ZhihuAnswer(
            zhihu_id=self["zhihu_id"],
            url=self["url"],
            question_id=self["question_id"],
            author_id=self["author_id"],
            content=self["content"],
            parise_num=self["parise_num"],
            comments_num=self["comments_num"],
            create_time=self["create_time"],
            update_time=self["update_time"],
            crawl_time=self["crawl_time"]
        )

        return item_sql


######################################
# Lagou
######################################


def remove_splash(value):
    return value.replace("/", "")


def remove_tags(value):
    return value


def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip() != "查看地图"]
    return "".join(addr_list)


class LagouJobItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()


class LagouJobItem(scrapy.Item):
    #拉勾网职位信息
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    work_years = scrapy.Field(
        input_processor = MapCompose(remove_splash),
    )
    degree_need = scrapy.Field(
        input_processor = MapCompose(remove_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr),
    )
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    tags = scrapy.Field(
        input_processor = Join(",")
    )
    crawl_time = scrapy.Field()

    def insert_to_mysql(self):
        item_sql = LagouPosition(
            title=self["title"],
            url=self["url"],
            url_object_id=self["url_object_id"],
            salary=self["salary"],
            work_years=self["work_years"],
            job_city=self["job_city"],
            degree_need=self["degree_need"],
            job_type=self["job_type"],
            publish_time=self["publish_time"],
            job_advantage=self["job_advantage"],
            job_desc=self["job_desc"],
            job_addr=self["job_addr"],
            company_name=self["company_name"],
            company_url=self["company_url"],
            tags=self["tags"],
            crawl_time=self["crawl_time"],
        )
        return item_sql


######################################
# Huxiu
######################################


class HuxiuItem(scrapy.Item):
    """虎嗅网Item"""
    title = scrapy.Field(
        input_processor=MapCompose(remove_blank)
    )                           # 标题
    link = scrapy.Field()       # 链接
    desc = scrapy.Field()       # 简述
    published = scrapy.Field()  # 发布时间

    def insert_to_mysql(self):
        item_sql = Huxiu(
            title=self["title"],
            link=self["link"].encode("utf-8"),
            desc=self["desc"].encode("utf-8"),
            published=self["published"].encode("utf-8"))
        return item_sql


##########################################
# ttxsgoto.github.io
##########################################


class TtxsgotoItem(scrapy.Item):

    title = scrapy.Field()          # 标题
    url = scrapy.Field()            # url
    publish = scrapy.Field()        # 发布日期
    content = scrapy.Field()        # 内容
    classify = scrapy.Field(        # 分类
        output_processor=Join(',')
    )
    lable = scrapy.Field()          # 标签
    create_time = scrapy.Field()    # 创建时间

    def insert_to_mysql(self):
        item_sql = TtxsgotoBlog(
            title=self["title"],
            url=self["url"],
            publish=self["publish"],
            content=self["content"],
            classify=self["classify"],
            lable=self["lable"],
            create_time=self["create_time"]
        )
        return item_sql
