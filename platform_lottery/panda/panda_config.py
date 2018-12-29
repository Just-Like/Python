#!/usr/bin/env python
# coding:utf-8
"""
@Auth ： Just
@File : panda_config.py
@Date : 2018/10/17
"""
import config
import logging

class PDConfig(config.CurrentConfig):
	"""平台配置文件"""

	platform='panda'
	#log
	log_file = 'log/panda.log'
	log_level = logging.INFO


	#api
	index_url = 'http://www.panda.tv/all'
	page_url = 'http://www.panda.tv/live_lists?status=2&token=&pageno={page}&pagenum=120&order=top&_={milli_time_stamp}'
	lottery_url = 'http://roll.panda.tv/meepo/user/going?token=&hostid={rid}&_={milli_time_stamp}'

	#爬取频率(一轮爬取完毕后等待多少s后再重新爬取)
	crawl_frequency = 1200
