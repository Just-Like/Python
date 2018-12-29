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
	def __init__(self,config,LOG):
		self.config=config
		self.LOG=LOG

		#统计指标
		self.total_page = 0
		self.fail_page = 0
		self.category_count = 0
		self.total_room = 0
		self.total_lottery_room = 0
		self.fail_lottery_room = 0
		#--------------------------
		self.roomid=u''
		self.lottery_prize = u''
		self.platform=u''
		self.lottery_time = 0
		self.lottery_condition = u''
		self.lottery_members = 0
		self.create_time = int(time.time())
		self.lottery_status = 0
		self.lottery_datas=[]

	def scrapy(self,url,try_num=3,**kwargs):
		response=None
		try_num=Config.TRY_NUMS
		if not url:
			url=kwargs['url']
			kwargs.pop('url')
		try:
			temp={'data':'','method':'','Cookie':''}
			default_header={"user-agent":random.choice(Config.USER_AGENT)}
			for key in kwargs.keys():
				if key in temp:
					temp[key]=kwargs[key]
					kwargs.pop(key)
			header = dict(default_header, **kwargs)
			if temp.values().count('')==3:    #没有用cookie，也没有参数的
				response=requests.get(url,headers=header,verify=False,proxies=random.choice(Config.proxies))
			elif temp.values().count('')==2:  #只有cookies的
				response = requests.get(url,headers=header,cookies=temp['Cookie'],verify=False,proxies=random.choice(Config.proxies))
			elif temp.values().count('')==1:  #只有有参数的
				response=getattr(requests,temp['method'])(url,headers=header,data=temp['data'],verify=False,proxies=random.choice(Config.proxies))
			elif temp.values().count('')==0:  #有参数有cookies的
				response=getattr(requests,temp['method'])(url,headers=header,data=temp['data'],cookies=temp['Cookie'],verify=False,proxies=random.choice(Config.proxies))
		except Exception as e:
			self.LOG.error("爬取页面{url} 失败 msg:{msg}".format(url=url,msg=e.message))
			if (response==None and try_num!=0)  or (try_num!=0 and response!=None and response.status_code!=200):
				self.scrapy(url,try_num=(try_num-1),**kwargs)
		self.LOG.info("爬取页面{url} 完毕状态码{status_code} ".format(url=url,status_code=response.status_code))
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
				'create_time': self.create_time
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
				lottery.create_time = data['create_time']
			lottery.members = data['members']
			try:
				session.add(lottery)
				session.commit()
			except sqlalchemy.exc.SQLAlchemyError as e:
				session.rollback()
				message = "platform: {platform}插入数据库失败: {msg}".format(platform=self.config.platform, msg=e.message)
			finally:
				session.close()


