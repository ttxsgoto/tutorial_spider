# tutorial_spider scrapy 练习

#### 简单记录scrapy学习
- scrapy框架使用,主要包括(Spider, CrawlSpider)两个模块
- scrapy+selenium操作浏览器进行爬取工作
- 数据写入操作通过sqlalchemy模块完成

#### 爬取站点主要包括
- douban_250 - (Spider) 基础数据爬取
- huxiu - (Spider) 基础数据爬取
- jobbole -(Spider) 基础数据爬取
- lagou - (CrawlSpider) 基础数据爬取
- ttxsgoto - (Spider + Selenium) 操作浏览器完成基础数据爬取
- ttxsgoto01 - (Spider) 基础数据爬取
- zhihu - (Spider) 完成登录功能,并将cookie保存到文件中,在使用时通过cookie验证
