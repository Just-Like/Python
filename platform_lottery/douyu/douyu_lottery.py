#!/usr/bin/env python
# coding:utf-8
'''
@Auth ： Just
@File : douyu_lottery.py
@Date : 2018/8/29
'''

import json
import re
import time
import gevent
from gevent import monkey
monkey.patch_all()
from douyu_config import DYConfig as Config
from douyu_logger import DOUYU_LOTTERY_LOG as LOG
from base_lottery import BaseLottery
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class DouyuLottery(BaseLottery):
	def __init__(self):
		BaseLottery.__init__(self,Config,LOG)
		self.start_time=time.time()


	def get_all_rooms(self):
		index_res=self.scrapy(Config.index_url)
		if index_res:
			self.total_page=re.search(r'count:\s"(.*?)",',index_res.content).groups(0)[0]   #获取总的页数
		else:
			self.total_lottery_room=0
			LOG.error('获取总页数有误！！！')
		jobs=[gevent.spawn(self.scrapy,Config.page_url.format(page=i+1)) for i in xrange(int(self.total_page))]
		gevent.joinall(jobs)
		for job in jobs:
			if job.value:
				yield job.value.json()
			else:
				self.fail_page += 1

	def get_lottery_rooms(self):
		lottery_rooms=[]
		for content in self.get_all_rooms():
			try:
				if content['msg']=='success':
					datas=content['data']
					for room in datas['rl']:
						if room.get("icdata") is not None and room["icdata"].has_key("302"):
							lottery_rooms.append(room)
				else:
					self.fail_page+=1
			except Exception,e:
				self.fail_page+=1
				LOG.error('page_url 的内容有误 value:{content},msg:{msg}'.format(content=content,msg=e.message))
		self.total_lottery_room=len(lottery_rooms)
		return lottery_rooms

	def scapy_lottery_room(self):
		lottery_rooms=self.get_lottery_rooms()
		jobs = [gevent.spawn(self.scrapy, Config.lottery_url.format(roomid=roomid['rid'])) for roomid in lottery_rooms]
		gevent.joinall(jobs)
		for job in jobs:
			if job.value:
				if not job.value.content:
					self.fail_lottery_room+=1
				else:
					yield job.value
			else:
				self.fail_lottery_room+=1

	def get_lotteryInfo(self):
		prize_num = 0
		try:
			for content in self.scapy_lottery_room():
				if content is not None:
					content = content.json()
					if content["data"] is not None:
						content = content["data"]
						self.lottery_prize = content["prize_name"]
						self.roomid=content['room_id']
						self.platform=Config.platform
						if content.has_key("prize_num"):
							prize_num = content["prize_num"]
						if content["join_condition"].has_key("command_content"):
							self.lottery_condition = json.dumps({"command": content["join_condition"]["command_content"], "prize_num": prize_num,"lottery_range":content["join_condition"]["lottery_range"]})
						elif content["join_condition"].has_key("gift_id"):
							self.lottery_condition = json.dumps({"giftid": content["join_condition"]["gift_id"],"num": content["join_condition"]["gift_num"],"prize_num": prize_num,"lottery_range":content["join_condition"]["lottery_range"]})
						if int(content["stop_at"]) == 0:
							self.lottery_time = int(content["start_at"]) + content["join_condition"]["expire_time"]
						else:
							self.lottery_time = int(content["stop_at"])
					self.format_lottery_datas()
		except Exception as e:
			print e
			LOG.error("update platform info failed {msg}".format(msg=e.message))

	def run(self):
		self.get_lotteryInfo()
		self.update_lottery()
		LOG.info('总共{total_page}页，失败{fail_page}页，总共{total_lottery_room}间直播抽奖，失败{fail_lottery_room}间,耗时{times}'.format(total_page=self.total_page,fail_page=self.fail_page,total_lottery_room=self.total_lottery_room,fail_lottery_room=self.fail_lottery_room,times=str(time.time()-self.start_time)))









if __name__ == '__main__':
	while True:
		t=DouyuLottery()
		start_time=time.time()
		t.get_lotteryInfo()
		t.update_lottery()
		time.sleep(60)







