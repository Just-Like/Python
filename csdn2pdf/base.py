# -*- coding: utf-8 -*-
# @Time    : 2018/10/14 9:51
# @Author  : Just
# @Email   : 2069298611@qq.com
# @File    : base.py
# @Software: PyCharm Community Edition
import re
import threading
import requests
import random
import hashlib
from config import *
from logger import LOG
class base(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def randHeader(self):
        header = {
            'Connection': head_connection[0],
            'Accept': head_accept[0],
            'Accept-Language': head_accept_language[1],
            'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))]
        }
        return header

    def scrapy(self,url,headers=None,try_nums=3):
        response=None
        if 'http' not in url:url='https:'+url
        try:
            headers=headers if headers else self.randHeader()
            response=requests.get(url,headers=headers)
            if response.status_code != 200:
                if try_nums > 0:
                    return self.scrapy(url, headers, try_nums - 1)
        except Exception as e:
            LOG.error('爬取页面失败url:{url},msg:{msg}'.format(url=url,msg=e.message))
            if try_nums>0:
                return self.scrapy(url,headers, try_nums - 1)
        return response

    def getmd5(self,str):
        m = hashlib.md5()
        m.update(str.encode('utf-8'))
        return m.hexdigest()[8:-8]


    def getfilecount(self,path):
        ls = os.listdir(path)
        count = 0
        for i in ls:
            if os.path.isfile(os.path.join(path, i)):
                count += 1
        return count


    def get_articl(self):
        pass

    def down_all_img(self):
        pass

    def save_pdf(self):
        pass

    def run(self):
        self.get_articl()
        self.down_all_img()
        self.save_pdf()






