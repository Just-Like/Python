#!/usr/bin/env python
# coding:utf-8
'''
@Auth ： Just
@File : douyu_logger.py
@Date : 2018/8/29
'''
from douyu_config import DYConfig
from logging import handlers,Formatter,getLogger

douyu_handler = handlers.RotatingFileHandler(DYConfig.log_file, maxBytes=50 * 1024 * 1024, backupCount=10)
fmt = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s'

formatter = Formatter(fmt)
douyu_handler.setFormatter(formatter)

DOUYU_LOTTERY_LOG = getLogger('douyu_lottery')
DOUYU_LOTTERY_LOG.addHandler(douyu_handler)
DOUYU_LOTTERY_LOG.setLevel(DYConfig.log_level)