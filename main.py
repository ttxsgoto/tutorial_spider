#!/usr/bin/env python
# coding: utf-8

from scrapy.cmdline import execute

import sys, os
"""
from scrapy import cmdline

name = 'douban_movie'
cmd = 'scrapy crawl {}'.format(name)

cmdline.execute(cmd.split())
"""

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(['scrapy', 'crawl', 'jobbole'])       # done
# execute(['scrapy', 'crawl', 'douban_250'])    # done
execute(['scrapy', 'crawl', 'zhihu'])         # done
# execute(['scrapy', 'crawl', 'lagou'])         # done
# execute(['scrapy', 'crawl', 'huxiu'])         # done
# execute(['scrapy', 'crawl', 'ttxsgoto'])      # done    scrapy + selenium
# execute(['scrapy', 'crawl', 'ttxsgoto01'])    # done

# 导出为json,csv等格式数据
# scrapy crawl douban_250 -o douban.csv
# 进入shell添加user-agent
# scrapy shell -s USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36" https://movie.douban.com/top250

