#!/usr/bin/env python
# coding: utf-8

import datetime
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Date
from sqlalchemy.orm import sessionmaker

from tutorial_spider.settings import MYSQL_DATABASE


def db_connect():
    return create_engine(URL(**MYSQL_DATABASE), echo=False)


def _get_now():
    return datetime.datetime.now()


def create_news_table(engine):
    """"""
    Base.metadata.create_all(engine)

Base = declarative_base()


class Huxiu(Base):
    """虎嗅网数据模型"""
    __tablename__ = 'spider_huxiu'

    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    link = Column(String(128))
    desc = Column(Text)
    published = Column(String(32))
    created_time = Column(DateTime, default=_get_now)


class Movietop250(Base):
    """豆瓣电影250模型"""
    __tablename__ = 'spider_movietop250'

    id = Column(Integer, primary_key=True)
    num = Column(String(10))
    movie_detail_url = Column(String(128))
    img_url = Column(String(128))
    img_file_path = Column(String(256))
    name = Column(String(512))
    grade = Column(String(10))
    comment = Column(String(256))
    info = Column(Text)
    created_time = Column(DateTime, default=_get_now)


class LagouPosition(Base):
    """拉勾职位模型"""
    __tablename__ = 'spider_lagouposition'

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    url = Column(String(128))
    url_object_id = Column(String(64))
    salary = Column(String(32))
    job_city = Column(String(64))
    work_years = Column(String(64))
    degree_need = Column(String(64))
    job_type = Column(String(64))
    publish_time = Column(String(32))
    job_advantage = Column(String(256))
    job_desc = Column(Text)
    job_addr = Column(Text)
    company_name = Column(String(256))
    company_url = Column(String(128))
    tags = Column(String(128))
    crawl_time = Column(DateTime, default=_get_now)
    created_time = Column(DateTime, default=_get_now)


class ZhihuQuestion(Base):
    """知乎问题模型"""
    __tablename__ = 'spider_zhihuquestion'

    id = Column(Integer, primary_key=True)
    zhihu_id = Column(String(32))       # 知乎id
    topics = Column(String(128))        # 主题
    url = Column(String(128))           # url
    title = Column(String(256))         # 标题
    content = Column(Text)              # 内容
    answer_num = Column(String(32))     # 回答数量
    comments_num = Column(String(32))   # 评论数量
    watch_user_num = Column(String(32)) # 关注者数量
    click_num = Column(String(32))      # 浏览数量
    crawl_time = Column(String(32))     # 爬取时间


class ZhihuAnswer(Base):
    """知乎回答模型"""
    __tablename__ = 'spider_zhihuanswer'

    id = Column(Integer, primary_key=True)
    zhihu_id = Column(String(32))       # 知乎id
    url = Column(String(128))           # url
    question_id = Column(String(32))    # 问题id
    author_id = Column(String(256))     # 作者id
    content = Column(Text)              # 内容
    parise_num = Column(String(32))     # 点赞数量
    comments_num = Column(String(32))   # 评论数量
    create_time = Column(String(32))    # 创建时间
    update_time = Column(String(32))    # 更新时间
    crawl_time = Column(String(32))     # 爬取时间


class TtxsgotoBlog(Base):
    __tablename__ = 'spider_ttxsgotoblog'
    id = Column(Integer, primary_key=True)
    title = Column(String(32))          # 标题
    url = Column(String(128))           # url
    publish = Column(String(32))        # 发布日期
    content = Column(Text)              # 内容
    classify = Column(String(32))       # 分类
    lable = Column(String(32))          # 标签
    create_time = Column(String(32))    # 创建时间


if __name__ == "__main__":
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    url = 'https://www.huxiu.com/article/225168.html'
    # 用于判断是否已经插入过该数据
    item_sql = session.query(Huxiu).filter(Huxiu.link == url).first()
    if item_sql:
        print('item_sql')
        print(item_sql.link)
    else:
        print('else')
    # for instance in xxx:
    #     print(instance.published)

    # for instance in session.query(Huxiu).all():
    #     print(instance.title, instance.link)



