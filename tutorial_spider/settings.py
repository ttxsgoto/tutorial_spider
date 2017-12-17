# -*- coding: utf-8 -*-

# Scrapy settings for tutorial_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import logging
import os
import sys

BOT_NAME = 'tutorial_spider'

SPIDER_MODULES = ['tutorial_spider.spiders']
NEWSPIDER_MODULE = 'tutorial_spider.spiders'
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'tutorial_spider'))      # 将目录设置到python path当中
FILE_DIR = os.path.join(BASE_DIR, 'files')
if not os.path.exists(FILE_DIR):
    os.mkdir(FILE_DIR)

# 文件导出中文, 设置字符集
FEED_EXPORT_ENCODING = 'utf-8'


# 自动传递cookies与打印cookies设置
COOKIES_ENABLES = True
# COOKIES_DEBUG = True
COOKIE_FILE = os.path.join(FILE_DIR, 'cookies.txt')    # cookie 存放目录

#USER_AGENT = 'tutorial_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True
ROBOTSTXT_OBEY = False

# 定义使用哪种user-agent
RANDOM_UA_TYPE = 'random'


USER_AGENT_LIST=[
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:57.0) Gecko/20100101 Firefox/57.0"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
]
###########################################
# logging 配置
# spider中使用:
# import logging
# logger = logging.getLogger(__name__)
# logger.info("logger info")
###########################################
LOG_DIR = os.path.join(PROJECT_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
LOG_ENABLED = True
LOG_ENCODING = "utf-8"
LOG_LEVEL = logging.DEBUG
LOG_FILE = os.path.join(LOG_DIR, 'spider.log')
LOG_STDOUT = True
LOG_FORMAT= '%(levelname)s %(asctime)s [%(name)s:%(module)s:%(funcName)s:%(lineno)s] [%(exc_info)s] %(message)s'
LOG_DATEFORMAT = "%Y-%m-%d %H:%M:%S"

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'tutorial_spider.middlewares.TutorialSpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    'tutorial_spider.middlewares.MyCustomDownloaderMiddleware': 543,
#     'tutorial_spider.middlewares.AutoRandomUserAgentMiddlware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'tutorial_spider.middlewares.RandomUserAgentMiddleware': 543,
    'tutorial_spider.middlewares.JSPageMiddleware': 1,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'tutorial_spider.pipelines.TutorialSpiderPipeline': 300,

   # Jobbole
   'tutorial_spider.pipelines.ArticleImagePipeline': 100,
   'tutorial_spider.pipelines.ArticlespiderPipeline': 200,
   'tutorial_spider.pipelines.JsonWithEncodingPipeline': 300,
   # 'tutorial_spider.pipelines.JsonExporterPipline': 400,
   # 'tutorial_spider.pipelines.MysqlPipeline': 500,
   # 'tutorial_spider.pipelines.MysqlTwistedPipline': 600,
   # 'scrapy.pipelines.images.ImagesPipeline': 100,

   # doubanmovietop250
   #  'tutorial_spider.pipelines.Movietop250Pipeline': 1,
    # 'tutorial_spider.pipelines.Movietop250MysqlPipeline': 25,
    # 'tutorial_spider.pipelines.Movietop250MysqlAsynPipeline': 20,
    # 'tutorial_spider.pipelines.Movietop250MyslqchemyPipeline': 20,
    # 'tutorial_spider.pipelines.Movietop250MongdbPipeline': 10,
    # 'tutorial_spider.pipelines.Movietop250JsonPipeline': 10,

    # zhihu
    # 'tutorial_spider.pipelines.ZhihuJsonPipeline': 10,
    # 'tutorial_spider.pipelines.ZhihuQuestionMyslqchemyPipeline': 20,
    # 'tutorial_spider.pipelines.ZhihuAnswerMyslqchemyPipeline': 30,

    # lagou
    # 'tutorial_spider.pipelines.LagouPostionMysqlchemyPipeline': 10,

}

# 图片下载相关设置
IMAGES_URLS_FIELD = 'front_image_url'       # 需要定义images_url,默认的为image_urls
IMAGES_STORE = os.path.join(PROJECT_DIR, 'images')
MAGES_EXPIRES = 30  # 30天内抓取的都不会被重抓
IMAGES_MIN_HEIGHT = 100
IMAGES_MIN_WIDTH = 100
# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# 启用AutoThrottle扩展
AUTOTHROTTLE_ENABLED = True
# The initial download delay
# 初始下载延迟(单位:秒) 默认为5秒
AUTOTHROTTLE_START_DELAY = 10
# The maximum download delay to be set in case of high latencies
# 在高延迟情况下最大的下载延迟(单位秒)
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AutoThrottle调试(debug)模式，展示每个接收到的response
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# MYSQL相关配置
MYSQL_DATABASE = {
    'drivername': 'mysql',
    'host': '127.0.0.1',
    'port': '3307',
    'username': 'root',
    'password': 'root',
    'database': 'py3_spirder',
    'query': {'charset': 'utf8'}
}

MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'py3_spirder'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_PORT = 3307

# MONGODB相关配置
MONGODB_HOST='127.0.0.1'
MONGODB_PORT=27017
MONGODB_DBNAME='py3_spirder'
MONGODB_DOCNAME='movietop250'

