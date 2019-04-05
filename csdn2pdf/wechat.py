# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
from lxml import etree
import pdfkit
import random
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'https://mp.weixin.qq.com/s/AulqorMExX91I3MMnUCRew'
# 开始爬取第一个页面（改成调用爬取程序）
options = {
    'encoding': "utf-8",
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "lxml")
body = soup.find("html")
imgs = body.find_all("img")
for img in imgs:
    data_src = img.get('data-src')
    print(data_src)
    if data_src != None:
        img['src'] = str(data_src)
# print(body)
fileName = 'pdffile' + '1212' + '.pdf'
print(fileName)

path_wk = r'G:\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wk)
pdfkit.from_string(str(body), fileName, options=options,configuration=config)
print("123")




#判断是否统一目录生成pdf文件
filepath = './' + fileName
print(filepath)
answer = os.path.exists(filepath)
print(answer)
#正常的调用上传接口
