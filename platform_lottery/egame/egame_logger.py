#!/usr/bin/env python
# coding:utf-8
'''
@Auth ： Just
@File : douyu_logger.py
@Date : 2018/8/9
'''
from egame_config import EGConfig
from logging import handlers,Formatter,getLogger

egame_handler = handlers.RotatingFileHandler(EGConfig.log_file, maxBytes=50 * 1024 * 1024, backupCount=10)
fmt = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s'

formatter = Formatter(fmt)
egame_handler.setFormatter(formatter)

EGAME_LOTTERY_LOG = getLogger('egame_lottery')
EGAME_LOTTERY_LOG.addHandler(egame_handler)
EGAME_LOTTERY_LOG.setLevel(EGConfig.log_level)