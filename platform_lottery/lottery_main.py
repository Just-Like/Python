#!/usr/bin/env python
# coding:utf-8
'''
@Auth ： Just
@File : lottery_main.py
@Date : 2018/8/29
'''
import sys
import time
import random

from douyu.douyu_config import DYConfig
from douyu.douyu_lottery import DouyuLottery
from egame.egame_config import EGConfig
from egame.egame_lottery import EgameLottery
from panda.panda_config import PDConfig
from panda.panda_lottery import PandaLottery

which_spider = {
	'douyu': [DYConfig, DouyuLottery],
	'egame': [EGConfig, EgameLottery],
	'panda': [PDConfig, PandaLottery]
}

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "ERROR: param length is {length}, need 2 or more!".format(length=len(sys.argv))
		sys.exit()
	spider_name = sys.argv[1]
	while True:
		crawl_frequency = which_spider[spider_name][0].crawl_frequency
		lottery_class = which_spider[spider_name][1]
		start_Time = time.time()
		spider = lottery_class()
		spider.run()
		time.sleep(random.randrange(crawl_frequency,crawl_frequency+30))
