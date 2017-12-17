# -*- coding: utf-8 -*-
import datetime
import json
import os
import re
import time
from urllib import parse
import scrapy
from scrapy.http.cookies import CookieJar
from scrapy.conf import settings
from scrapy.loader import ItemLoader

from tutorial_spider.items import ZhihuQuestionItem, ZhihuAnswerItem
from tutorial_spider.utils.common import get_cookie_from_file

cookie_jar = CookieJar()

# scrap 会自动将cookie保存起来,我们不需要额外的代码来实现保存


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    custom_settings = {
        "ITEM_PIPELINES": {
            'tutorial_spider.pipelines.ZhihuJsonPipeline': 10,
            'tutorial_spider.pipelines.ZhihuQuestionMyslqchemyPipeline': 20,
            'tutorial_spider.pipelines.ZhihuAnswerMyslqchemyPipeline': 30,
        },
    }

    agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:57.0) Gecko/20100101 Firefox/57.0"
    headers = {
        'HOST': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com',
        'User-Agent': agent
    }

    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"
    cookie = get_cookie_from_file()

    def parse(self, response):
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                # 如果提取到question相关的页面则下载后交由提取函数进行提取
                request_url = match_obj.group(1)
                yield scrapy.Request(url=request_url,
                                     callback=self.parse_question)
            else:
                # 如果不是question页面则直接进一步跟踪
                yield scrapy.Request(url=url,
                                     callback=self.parse)

    def parse_question(self, response):
        """question 数据爬取详情"""
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
        if match_obj:
            question_id = int(match_obj.group(2))
        else:
            question_id = 0
        item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
        item_loader.add_css('title', '.QuestionHeader .QuestionHeader-title::text')
        item_loader.add_css('content', '.QuestionHeader-detail .RichText::text')
        item_loader.add_value('url', response.url)
        item_loader.add_value('zhihu_id', question_id)
        item_loader.add_css('answer_num', '.List-headerText span::text')
        item_loader.add_css('comments_num', '.QuestionHeader-Comment button::text')
        item_loader.add_css('watch_user_num', '.NumberBoard-value::text')
        item_loader.add_css('click_num', '.NumberBoard-value::text')
        # item_loader.add_css('topics', 'QuestionHeader-topics .Popover div::text')   # 现在还没有取到
        item_loader.add_value('topics', response.url)
        item_loader.add_value('crawl_time', now_time)
        question_item = item_loader.load_item()
        yield question_item

        yield scrapy.Request(url=self.start_answer_url.format(question_id, 20, 0),
                             cookies= self.cookie,
                             callback=self.parse_answer)

    def parse_answer(self, response):
        answer_json = json.loads(response.text)
        is_end = answer_json["paging"]["is_end"]
        next_url = answer_json["paging"]["next"]

        for answer in answer_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if "content" in answer else None
            answer_item["parise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield answer_item

        if not is_end:
            yield scrapy.Request(url=next_url,
                                 callback=self.parse_answer)

    def start_requests(self):
        return [scrapy.Request(url='https://www.zhihu.com',
                               headers=self.headers,
                               cookies=self.cookie,
                               callback=self.cookie_check_login)]   # 从登录页面获取数据,然后在传递给login函数处理

    def login(self, response):
        match_obj = re.search('.*input type="hidden" name="_xsrf" value="(.*?)"', response.text)    # re.DOTALL 匹配全文
        xsrf = ''
        if match_obj:
            xsrf = match_obj.group(1)
        if xsrf:
            post_data = {
                '_xsrf': xsrf,
                'email': '1824841486@qq.com',
                'password': '******',
                'captcha': ''
            }

            ########### 验证码获取逻辑 ###########
            t = str(int(time.time() * 1000))
            captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
            yield scrapy.Request(url=captcha_url,
                                 headers=self.headers,
                                 meta={'post_data': post_data,
                                       'cookiejar': response.meta['cookiejar']
                                       },
                                 callback=self.login_after_captcha)

    def login_after_captcha(self, response):
        with open("captcha.jpg", "wb") as f:
            f.write(response.body)
            f.close()
        from PIL import Image
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            pass
        captcha = input("输入验证码\n>")
        post_url = 'https://www.zhihu.com/login/email'
        post_data = response.meta.get('post_data', {})  # 通过meta将post_data传递过来
        post_data['captcha'] = captcha
        return [scrapy.FormRequest(  # 使用formrequest来登录
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            meta={'cookiejar': response.meta['cookiejar']},
            callback=self.check_login
        )]

    def check_login(self, response):    # 函数中如果不写回调函数callback,默认将进入parse函数解析
        """用户名密码登录方式,验证登录是否成功"""
        cookie_jar = response.meta['cookiejar']
        cookie_jar.extract_cookies(response, response.request)
        cookie_file = settings['COOKIE_FILE']
        if os.path.exists(cookie_file):
            os.remove(cookie_file)
        with open(cookie_file, 'w') as f:
            for cookie in cookie_jar:
                f.write(str(cookie) + '\n')
        for url in self.start_urls:
            yield scrapy.Request(url=url,
                                 headers=self.headers,
                                 meta={'cookiejar': response.meta['cookiejar']},
                                 dont_filter=True)
            # yield self.make_requests_from_url(url)

    def cookie_check_login(self, response):
        """cookie方式验证登录是否成功"""
        text = response.text
        if u"登录" not in text and u"注册" not in text:
            for url in self.start_urls:
                yield scrapy.Request(url=url,
                                     headers=self.headers,
                                     dont_filter=True)
            #     # yield self.make_requests_from_url(url)
        else:
            yield scrapy.Request(url='https://www.zhihu.com/#signin',
                                 headers=self.headers,
                                 meta={'cookiejar': cookie_jar},
                                 dont_filter=True,  # 表示此请求不应由调度程序过滤。当想要多次执行相同的请求时忽略重复过滤器时使用
                                 callback=self.login)  # 从登录页面获取数据,然后在传递给login函数处理
