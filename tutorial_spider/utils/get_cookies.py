#!/usr/bin/env python
# coding: utf-8
"""
Describe:
    - 将登录后的cookie转换成 python 可识别的cookie dict对象
"""


class transCookie(object):
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

if __name__ == "__main__":
    cookie = """
    d_c0="AGDCjkuf7wqPTgTmnn-p6Upe3_OhUImrpsw=|1480659468"; _xsrf=485af44997efb85437fb52af37cc8023; _zap=8187f0ff-23cb-44fb-a21a-838d3fcd4144; aliyungf_tc=AQAAAHESUCos+woAh210dqCRgS31KZ/b; q_c1=4e3e5576b5a84c77bc26c99aa4372f72|1506475390000|1480659468000; q_c1=4e3e5576b5a84c77bc26c99aa4372f72|1511140659000|1480659468000; s-t=autocomplete; r_cap_id="NDBkMGIyMGMyODg0NDU2YWE3Nzc5ZTZmZmFmMmNmMWI=|1512463315|5409456a2809b43633f001fe4ea01011cadd096c"; cap_id="ODgxOWUxNDVlZTg2NGRiODllMmZhZWYyNzdlZjczMTc=|1512463315|0d85e4d6508e19e543fbd2bef34609fd7f422958"; __utma=51854390.1932561857.1512462688.1512462688.1512462688.1; __utmb=51854390.0.10.1512462688; __utmc=51854390; __utmz=51854390.1512462688.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.000--|3=entry_date=20161202=1; _xsrf=485af44997efb85437fb52af37cc8023; z_c0=Mi4xOTBuNkFBQUFBQUFBWU1LT1M1X3ZDaGNBQUFCaEFsVk5XNm9UV3dBZGl4WWFkUkU2Y3ViM2M2azdONTlKZVd3WThn|1512463451|704488a44d23a72039da8d32dca0631ab7d12561
    """
    trans = transCookie(cookie)
    print(trans.stringToDict())

