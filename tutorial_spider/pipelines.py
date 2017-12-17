# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import copy
import hashlib
import json
import codecs   # 主要注意文件编码
from contextlib import contextmanager

import MySQLdb
import MySQLdb.cursors
import pymongo
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from scrapy.utils.python import to_bytes
from sqlalchemy.orm import sessionmaker
from twisted.enterprise import adbapi
from scrapy.http import Request

from scrapy.conf import settings
from tutorial_spider.models import db_connect, create_news_table, Huxiu, Movietop250
import logging
logger = logging.getLogger(__name__)


@contextmanager
def session_scope(Session):
    session = Session()
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class BasicMyslqchemyPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        insert_sql = item.insert_to_mysql()
        with session_scope(self.Session) as session:
            session.add(insert_sql)
        # return item

    def close_spider(self, spider):
        pass


class TutorialSpiderPipeline(object):

    def __init__(self):
        self.f = open('../douban.csv', 'w')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False)
        self.f.write(content.encode('utf-8'))
        return item

    def close_spider(self, spider):
        self.f.close()


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipeline(ImagesPipeline):

    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value['path']
            item['front_image_path'] = image_file_path
        return item


class JsonWithEncodingPipeline(object):
    # 自定义json文件导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # ensure_ascii 主要处理中文
        lines = json.dumps(dict(item), ensure_ascii=False)
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        """
        调用完成后,关闭file
        :param spider:
        :return:
        """
        self.file.close()


class JsonExporterPipline(object):
    # 调用scrapy提供的json export 导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    """mysql同步,自定义mysql写入"""
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'article_spirder', 3307, charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(title, url, create_date, fav_nums)
            Values (%s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, item['title'], item['url'], item['create_date'], item['fav_nums'])
        self.conn.commit()


class MysqlTwistedPipline(object):
    """使用twisted将mysql异步"""

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        """该方法用于读取settings配置"""
        dbparms = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWORD'],
            port = settings['MYSQL_PORT'],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
        )

        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        """将插入变成异步操作"""
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) # 处理异常

    def handle_error(self, failure, item, spider):
        """处理异步插入异常"""
        print (failure)

    def do_insert(self, cursor, item):
        """
        执行具体插入数据
        """
        insert_sql = """
            insert into jobbole_article(title, url, create_date, fav_nums)
            Values (%s, %s, %s, %s)
        """
        cursor.execute(insert_sql, item['title'], item['url'], item['create_date'], item['fav_nums'])


########################################################
#  MovieTop250
########################################################

class Movietop250Pipeline(ImagesPipeline):
    """添加图片存储目录"""
    def get_media_requests(self, item, info):
        for image_url in item['img_url']:
            yield scrapy.Request(image_url, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)

        image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
        return 'full/movie250/%s.jpg' % (image_guid)

    def item_completed(self, results, item, info):
        if "img_url" in item:
            item['img_file_path'] = [x['path'] for ok, x in results if ok]
            if not item['img_file_path']:
                # item['img_file_path'] = ''
                # return item
                raise DropItem("Item contains no images")
        return item


class Movietop250MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'py3_spirder', 3307, charset='utf8',
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = """
            insert into movietop250(num, movie_detail_url, img_url, name, grade, comment, info, img_file_path)
               values (%s, %s, %s, %s, %s, %s, %s, %s)
           """
        params = (item['num'], item['movie_detail_url'], item['img_url'],
                  item['name'], item['grade'], item['comment'], item['info'],
                  item['img_file_path'])
        self.cursor.execute(sql, params)
        self.conn.commit()
        return item


class Movietop250MysqlAsynPipeline(object):
    """导入到Mongodb"""
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        """该方法用于读取settings配置"""
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            port=settings['MYSQL_PORT'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )

        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        """将插入变成异步操作"""
        asynItem = copy.deepcopy(item)
        # time.sleep(0.1)
        query = self.dbpool.runInteraction(self.do_insert, asynItem)
        query.addErrback(self.handle_error, item, spider)  # 处理异常
        query.addBoth(lambda _: item)
        return item

    def handle_error(self, failure, item, spider):
        """处理异步插入异常"""
        print(failure)

    def do_insert(self, cursor, item):
        sql = """
         insert into movietop250(num, movie_detail_url, img_url, name, grade, comment, info, img_file_path)
            values (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (item['num'], item['movie_detail_url'], item['img_url'],
                  item['name'], item['grade'], item['comment'], item['info'],
                  item['img_file_path'])
        cursor.execute(sql, params)

    def close_spider(self, spider):
        """Discard the database pool on spider close"""
        self.dbpool.close()


class Movietop250MongdbPipeline(object):
    """导入到Mongodb"""
    def __init__(self, mongo_uri, mongo_db, port, collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.port = port
        self.collection_name = collection_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=settings.get('MONGODB_HOST'),
            port=settings.get('MONGODB_PORT'),
            mongo_db=settings.get('MONGODB_DBNAME', 'items'),
            collection_name = settings.get('MONGODB_DOCNAME')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri, self.port)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item1 = dict(item)
        self.db[self.collection_name].insert(item1)
        return item


class Movietop250JsonPipeline(object):
    """自定义json文件导出"""
    def __init__(self):
        self.file = codecs.open('movietop250.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # ensure_ascii 主要处理中文
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        """
        调用完成后,关闭file
        :param spider:
        :return:
        """
        self.file.close()


class ZhihuJsonPipeline(object):
    """自定义json文件导出"""
    def __init__(self):
        self.file = codecs.open('zhihu.json', 'w+', encoding='utf-8')

    def process_item(self, item, spider):
        # ensure_ascii 主要处理中文
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        """
        调用完成后,关闭file
        :param spider:
        :return:
        """
        self.file.close()


class ZhihuQuestionMyslqchemyPipeline(BasicMyslqchemyPipeline):
    """保存知乎问题到数据库"""
    pass


class ZhihuAnswerMyslqchemyPipeline(BasicMyslqchemyPipeline):
    """保存知乎回答到数据库"""
    pass


class HuxiuMyslqchemyPipeline(BasicMyslqchemyPipeline):
    """保存虎嗅到数据库"""

    def __init__(self):
        super(HuxiuMyslqchemyPipeline, self).__init__()

    def process_item(self, item, spider):
        insert_sql = item.insert_to_mysql()
        with session_scope(self.Session) as session:
            data = session.query(Huxiu).filter(Huxiu.link == item["link"].encode("utf-8"),).first()
            session.add(insert_sql) if not data else None
        return item


class Movietop250MyslqchemyPipeline(BasicMyslqchemyPipeline):
    """保存豆瓣250到数据库"""
    def __init__(self):
        super(Movietop250MyslqchemyPipeline, self).__init__()

    def process_item(self, item, spider):
        insert_sql = item.insert_to_mysql()
        with session_scope(self.Session) as session:
            # 判断该数据是否已经写入过数据库,如果写入过,就不在写入
            data = session.query(Movietop250).filter(Movietop250.movie_detail_url == item["movie_detail_url"].encode("utf-8"), ).first()
            session.add(insert_sql) if not data else None
        return item


class LagouPostionMysqlchemyPipeline(BasicMyslqchemyPipeline):
    """保存拉勾职位到数据库"""
    pass


class TtxsgotoFilterPipeline(object):
    """过滤某些item"""

    def process_item(self, item, spider):
        if item['title'] == 'Python Selenium模块':
            raise DropItem('Drop item--->', item)
        else:
            return item


class TtxsgotoBlogMysqlchemyPipeline(BasicMyslqchemyPipeline):
    """保存ttxsgoto Blog到数据库"""
    pass

