#!/usr/bin/env python
# coding:utf-8
'''
@Auth ： Just
@File : base_lottery.py
@Date : 2018/8/29
'''
import time
import random
import requests
import sqlalchemy
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from config import Config
from db import DB_Session
from orm.lottery import Lottery
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
class BaseLottery():
	def __init__(self, config, log):
		self.config = config
		self.LOG = log

		# 统计指标
		self.total_page = 0
		self.fail_page = 0
		self.category_count = 0
		self.total_room = 0
		self.total_lottery_room = 0
		self.fail_lottery_room = 0
		# --------------------------
		# 数据库字段
		self.roomid = u''
		self.lottery_prize = u''
		self.platform = u''
		self.lottery_time = 0
		self.lottery_condition = u''
		self.lottery_members = 0
		self.lottery_status = 0
		self.lottery_datas = []

	def scrapy(self, url, try_num=3, **kwargs):
		"""
		:param url:  需要爬取的url地址
		:param try_num: 爬取重爬次数
		:param kwargs:  cookies、data、headers等参数
		:return:  None or response
		"""
		response = None
		try:
			default_header = {"user-agent": random.choice(Config.USER_AGENT)}
			response = requests.get(url, headers=default_header, verify=False, proxies=random.choice(Config.proxies))
		except Exception as e:
			self.LOG.error("爬取页面{url} 失败 msg:{msg}".format(url=url, msg=e.message))
			if (response is None and try_num != 0) or (try_num != 0 and response is not None and response.status_code != 200):
				self.scrapy(url, try_num=(try_num-1), **kwargs)
		self.LOG.info("爬取页面{url} 完毕状态码{status_code} ".format(url=url, status_code=response.status_code))
		return response

	def format_lottery_datas(self):
		self.lottery_datas.append(
			{
				'room_id': self.roomid,
				'lottery_prize': self.lottery_prize,
				'platform': self.platform,
				'lottery_time': self.lottery_time,
				'condition': self.lottery_condition,
				'members': self.lottery_members,
			}

		)

	def update_lottery(self):
		session = DB_Session()
		for data in self.lottery_datas:
			try:
				lottery = session.query(Lottery).filter(Lottery.room_id == data['room_id'],
				                                        Lottery.platform == data['platform'],
				                                        Lottery.condition == data['condition'],
				                                        Lottery.lottery_time == data['lottery_time']).first()
			except sqlalchemy.exc.SQLAlchemyError as e:

				self.LOG.info("mysql query error: {msg}".format(msg=e.message))
				session.close()
				session = DB_Session()
				continue
			if not isinstance(lottery, Lottery):
				lottery = Lottery()
				lottery.room_id = data['room_id']
				lottery.lottery_prize = data['lottery_prize']
				lottery.platform = data['platform']
				lottery.lottery_time = data['lottery_time']
				lottery.condition = data['condition']
			lottery.members = data['members']
			try:
				session.add(lottery)
				session.commit()
			except sqlalchemy.exc.SQLAlchemyError as e:
				session.rollback()
				message = "platform: {platform}插入数据库失败: {msg}".format(platform=self.config.platform, msg=e.message)
				self.LOG.error(message)
		session.query(Lottery).filter(Lottery.platform == self.platform, Lottery.lottery_time < time.time()).delete()
		session.commit()
		session.close()



