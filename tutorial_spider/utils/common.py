#!/usr/bin/env python
# coding: utf-8

import hashlib
import re
from scrapy.conf import settings


def get_md5(url):
    if isinstance(url, str): # unicode
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def get_cookie_from_file():
    cookie_file = settings['COOKIE_FILE']
    with open(cookie_file, 'r') as f:
        cookiejar = f.read()
        p = re.compile(r'<Cookie (.*?) for .*?>')
        cookies = re.findall(p, cookiejar)
        cookies = (cookie.split('=', 1) for cookie in cookies)
        cookies = dict(cookies)
    return cookies


if __name__ == '__main__':
    url = 'https://movie.douban.com/subject/1292722/'
    print(get_md5(url))
    print(get_cookie_from_file())
