# -*- coding: utf-8 -*-
# @Time    : 2018/10/14 9:44
# @Author  : Just
# @Email   : 2069298611@qq.com
# @File    : logger.py
# @Software: PyCharm Community Edition
import logging
from config import LOG
from logging import handlers,Formatter,getLogger

handler=handlers.RotatingFileHandler(LOG,maxBytes=50 * 1024 * 1024, backupCount=10)
fmt = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s'
formatter=Formatter(fmt)
handler.setFormatter(formatter)
LOG=getLogger('csdn2pdf')
LOG.addHandler(handler)
LOG.setLevel(logging.INFO)

