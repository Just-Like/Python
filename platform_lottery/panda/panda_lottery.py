#!/usr/bin/env python
# coding:utf-8
'''
@Auth ： Just
@File : panda_lottery.py
@Date : 2018/10/17
'''
import json
import time
import gevent
import random
import functools
from gevent import monkey
monkey.patch_all()
import requests
from panda_config import PDConfig as Config
from panda_logger import PANDA_LOTTERY_LOG as LOG
from base_lottery import BaseLottery
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class PandaLottery(BaseLottery):
	def __init__(self):
		BaseLottery.__init__(self,Config,LOG)
		self.start_time=time.time()


	def scraping(self,url,try_num=3,ext_param=object):
		res = None
		User_Agent = [
			'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
			'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
			'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
			'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
			'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre',
			'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
		]
		headers = {"User-Agent": random.choice(User_Agent),
		           'Referer':'https://www.panda.tv/all'
		           }
		try:
			res = requests.get(url,headers=headers,proxies=random.choice(Config.proxies))
			if res.status_code != 200 and try_num>0:
				self.scraping(url,try_num=try_num-1)
		except Exception as e:
			LOG.error('爬取{url}页面失败 error:{error} '.format(url=url,error=e.message))
			if try_num>0:
				self.scraping(url,try_num=try_num-1)
		LOG.info('爬取{url}页面完毕 状态码{status_code}'.format(url=url,status_code=res.status_code))
		if ext_param == object:
			return res
		else:
			return res,ext_param


	def get_all_rooms(self):
		milli_time_stamp=str(int(time.time()*1000))
		first_page_url=Config.page_url.format(page=1,milli_time_stamp=milli_time_stamp)
		while 1 :
			flag=1
			first_page_content=self.scraping(first_page_url)
			if first_page_content or flag>5:
				break
			flag+=1
		try:
			if first_page_content:
				total_page=first_page_content.json()['data']['total']/120+1
				self.total_room=first_page_content.json()['data']['total']
				self.total_page=total_page
			jobs = [gevent.spawn(self.scraping, Config.page_url.format(page=i + 1,milli_time_stamp=str(int(time.time()*1000)))) for i in xrange(int(total_page))]
			gevent.joinall(jobs)
			for job in jobs:
				if job.value:
					yield job.value.json()
				else:
					self.fail_page += 1
		except Exception as e:
			LOG.error("爬取房间页面失败 error:{error}".format(error=e.message))

	def get_lottery_rooms(self):
		lottery_rooms = []
		try:
			for content in self.get_all_rooms():
				rooms=content.get('data').get('items')
				if rooms:
					for room in rooms:
						rollinfo = room.get('rollinfo') if isinstance(room.get('rollinfo'), list) else None
						if rollinfo is not None and 'meepo' in rollinfo:
							rid = room['userinfo']['rid']
							really_rid = room['id']
							lottery_rooms.append((rid,really_rid))
		except Exception as e:
			LOG.error("获取抽奖房间失败error:{error}".format(error=e.message))
		self.total_lottery= len(lottery_rooms)
		return lottery_rooms

	def scapy_lottery_room(self):
		lottery_rooms=self.get_lottery_rooms()
		jobs=[]
		try:
			for roomid in lottery_rooms:
				scraping= functools.partial(self.scraping, ext_param=roomid[1])
				url=Config.lottery_url.format(rid=str(roomid[0]), milli_time_stamp=str(int(time.time() * 1000)))
				i=gevent.spawn(scraping, url)
				jobs.append(i)
			gevent.joinall(jobs)
			for job in jobs:
				if job.value[0]:
					if not job.value[0].content:
						self.fail_lottery_room += 1
					else:
						yield job.value
				else:
					self.fail_lottery_room += 1
		except Exception as e:
			LOG.error("获取抽奖房间信息失败error:{error}".format(error=e.message))

	def get_lotteryInfo(self):
		for content in self.scapy_lottery_room():
			lottery_content=content[0].json()
			self.roomid=content[1]
			if lottery_content['data']!=[] and lottery_content["errno"] == 0:
				for data in lottery_content['data']:
					needgift_num=data['giftnum']
					need_giftid=data["need_giftid"]
					self.lottery_prize=data['giftname']
					self.lottery_time=data['endtime']
					self.lottery_condition=json.dumps({'giftid':need_giftid,'num':str(needgift_num)})
					self.lottery_members=data['gnum']
					#self.roomid=data['rid']
					self.platform = Config.platform
					self.create_time=int(time.time())
					self.lottery_status=1
					self.format_lottery_datas()
		self.total_lottery_room=len(self.lottery_datas)

	def run(self):
		self.get_lotteryInfo()
		self.update_lottery()
		LOG.info(
			'总共{total_page}页，失败{fail_page}页，总开播房间有{total_room}间，总共{total_lottery_room}间直播抽奖，失败{fail_lottery_room}间,耗时{times}'.format(
				total_page=self.total_page, fail_page=self.fail_page, total_lottery_room=self.total_lottery_room,
				total_room=self.total_room,fail_lottery_room=self.fail_lottery_room, times=str(time.time() - self.start_time)))



if __name__ == '__main__':
	p=PandaLottery()
	p.run()
