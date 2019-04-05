# -*- coding: utf-8 -*-
# @Time    : 2018/10/14 9:42
# @Author  : Just
# @Email   : 2069298611@qq.com
# @File    : main.py
# @Software: PyCharm Community Edition

import re
import gevent
import random
import pdfkit
import shutil
from gevent import monkey
monkey.patch_all()
from config import *
from lxml import etree
from base import base
from logger import LOG

class Csdn2pdf(base):
    def __init__(self,url):
        base.__init__(self)
        self.url=url
        self.content_Element=None
        self.img_urls = None
        self.articl_title=None
        self.articl_content_str=None
        self.hash_url=self.getmd5(url)
        self.img_sub_path=None



    def get_articl(self):
        url = self.url
        platform = re.findall('\.(.*?)\.', self.url)[0]
        scrapy_header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Connection': 'keep-alive',
            'Referer': url,
        }
        html = self.scrapy(url,headers=scrapy_header)
        LOG.info('开始爬取：{url}'.format(url=self.url))
        if not html:
            LOG.info('获取文章内容失败')
            print u'爬取页面失败'
            return
        tree = etree.HTML(html.content)
        content = tree.xpath(xpath_rule[platform]['content'])
        articl_title = tree.xpath(xpath_rule[platform]['title'])[0]
        articl_content_str = etree.tostring(content[0])
        self.content_Element = content[0]
        self.articl_title=articl_title
        self.articl_content_str=articl_content_str
        LOG.info('获取页面内容成功')

    def down_img(self,img_index,img_url):
        #host = re.findall('//(.*?)/',img_url)[0]
        img_header = {
            #'Host': host,
            'User-Agent': random.choice(head_user_agent),
            'Referer':self.url
        }
        res = self.scrapy(img_url,img_header)
        if res:
            file_name = self.hash_url+"_"+str(img_index)+'.jpg'
            path = os.path.join(self.img_sub_path,file_name)
            with open(path,'wb') as f:
                f.write(res.content)
        else:
            return 0

    def down_all_img(self):
        img_sub_path=os.path.join(IMGTMP,self.hash_url)
        if os.path.exists(img_sub_path): os.remove(img_sub_path)
        os.mkdir(img_sub_path)
        self.img_sub_path = img_sub_path
        img_urls=self.content_Element.xpath('.//img/@src|.//img/@data-original-src')
        print img_urls
        jobs = [gevent.spawn(self.down_img, *(img_index,img_url)) for img_index,img_url in enumerate(img_urls)]
        gevent.joinall(jobs, timeout=2)
        self.img_urls=img_urls
        imgs_cout=self.getfilecount(img_sub_path)
        LOG.info('文内图片下载完毕！！！共{url_cout}个img_url,下载成功{imgs_cout}张图片'.format(url_cout=len(img_urls),imgs_cout=imgs_cout))


    def save_pdf(self):
        articl_content_str=self.articl_content_str
        for img_index,img_url in enumerate(self.img_urls):
            img_name = self.hash_url + "_" + str(img_index) + '.jpg'
            articl_content_str=articl_content_str.replace(img_url,os.path.join(self.img_sub_path,img_name)).replace('data-original-src','src')
        path_wk = r'G:\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wk)
        file_name=os.path.join(PDF, self.articl_title + '.pdf')
        tmp_name=os.path.join(PDF,self.hash_url+'.pdf')
        if os.path.exists(tmp_name): os.remove(tmp_name)
        if os.path.exists(file_name): os.remove(file_name)
        try:
            pdfkit.from_string(articl_content_str,tmp_name , options=wkhtmltopdf_options, configuration=config)
            os.renames(tmp_name,file_name)
            shutil.rmtree(os.path.join(IMGTMP,self.hash_url))
        except Exception as e:
            LOG.error('转换失败{msg}'.format(msg=e.message))
        LOG.info('转换完毕！！！！')


    def main(self):
        self.get_articl()
        self.down_all_img()
        self.save_pdf()


if __name__ == '__main__':
    urls=['https://mp.weixin.qq.com/s/AulqorMExX91I3MMnUCRew']
    #urls=['https://www.jianshu.com/p/6957daa98e41?utm_campaign=maleskine&utm_content=note&utm_medium=pc_all_hots&utm_source=recommendation']
    for i in urls:
        t = Csdn2pdf(i)
        t.start()




