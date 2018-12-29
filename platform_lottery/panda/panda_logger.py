#!/usr/bin/env python
# coding:utf-8
'''
@Auth ： Just
@File : panda_logger.py
@Date : 2018/10/17
'''
from logging import getLogger,handlers,Formatter
from panda_config import PDConfig


PANDA_LOTTERY_LOG = getLogger('panda_lottery')
panda_handler = handlers.RotatingFileHandler(PDConfig.log_file,maxBytes=50 * 1024 *1024,backupCount=10)
fmt='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s'
formatter = Formatter(fmt)
panda_handler.setFormatter(formatter)

PANDA_LOTTERY_LOG.addHandler(panda_handler)
PANDA_LOTTERY_LOG.setLevel(PDConfig.log_level)