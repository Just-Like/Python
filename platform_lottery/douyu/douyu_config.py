#!/usr/bin/env python
# coding:utf-8
'''
@Auth ： Just
@File : douyu_config.py
@Date : 2018/8/29
'''
import config
import logging
class DYConfig(config.CurrentConfig):
	"""平台配置文件"""

	platform='douyu'
	#log
	log_file='log/douyu.log'
	log_level = logging.INFO

	# header config
	header_config={'referer':'https://www.douyu.com/directory/all'}
	#api
	index_url = 'https://www.douyu.com/directory/all'
	page_url = "https://www.douyu.com/gapi/rkc/directory/0_0/{page}"
	lottery_url = "https://www.douyu.com/member/lottery/activity_info?room_id={roomid}"

	crawl_frequency = 180