#!/usr/bin/env python
# coding:utf-8
'''
@Auth ： Just
@File : douyu_logger.py
@Date : 2018/8/9
'''

import json
import re
import time
import gevent
import requests
import threading
from gevent import monkey
monkey.patch_all()
from egame_config import EGConfig as Config
from egame_logger import EGAME_LOTTERY_LOG as LOG
from base_lottery import BaseLottery
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class EgameLottery(BaseLottery):
    def __init__(self):
        BaseLottery.__init__(self,Config,LOG)
        self.start_time=time.time()
        self.lottery_rooms=[]
    def get_category_list(self):
        url = Config.gamelist_url
        response = self.scrapy(url=url)
        if response:
            try:
                html = response.content
                result = re.findall('window.__NUXT__=(.*?);</script>',html)[0]
                json_result=json.loads(result)
                all_category_info=json_result.get('state').get("game").get('categoryList')[0].get('vecGames')
                all_app_id=[app_info['appid'] for app_info in all_category_info]
                self.category_count=len(all_app_id)
                LOG.info('获取房间分类成功，总共{category_count}个分类'.format(category_count=self.category_count))
                return all_app_id
            except Exception,e:
                LOG.error('获取房间分类失败！！！ msg:{msg}'.format(msg=e.message))
    def scrapy_single_category(self,appid):
        pageid=1
        LOG.info('开始爬取分类--{appid}'.format(appid=appid))
        try:
            url=Config.roomlist_url.format(pageid=pageid,appid=appid,timespamt=int(time.time())*1000)
            res=self.scrapy(url)
            total_room=res.json().get('data').get('key').get('retBody').get('data').get('total')
            self.total_room+=total_room
            res_times=total_room/40+1
            self.total_page+=(res_times-1)
            jobs = [gevent.spawn(self.scrapy, Config.roomlist_url.format(pageid=pageid,appid=appid,timespamt=int(time.time())*1000)) for pageid in xrange(1,res_times+1)]
            gevent.joinall(jobs)
            for job in jobs:
                if job.value:
                    live_data=job.value.json().get('data').get('key').get('retBody').get('data').get('live_data').get('live_list')
                    for room in live_data:
                        if room['program_res']['icon_tag']['priority'] == 10000300:
                            self.lottery_rooms.append(room['anchor_id'])
                            #print room['anchor_id']
                else:
                    self.fail_page += 1
        except Exception,e:
            LOG.error('爬取页面失败,msg:{}'.format(e.message))


    def get_all_lottery_room(self):
        all_app_id=self.get_category_list()
        threads=[]
        try:
            for id in all_app_id:
                t = threading.Thread(target=self.scrapy_single_category, args=(id,))
                t.start()
                threads.append(t)
            [t.join() for t in threads]
        except Exception,e:
            LOG.error('线程爬取页面信息失败:msg'.format(e.message))

    def get_all_lottery_info(self):
        self.get_all_lottery_room()
        self.total_lottery_room=len(self.lottery_rooms)
        urls=[Config.lotteryinfo_url.format(timestamp=int(time.time())*1000,anchor_id=anchor_id) for anchor_id in self.lottery_rooms]
        jobs=[gevent.spawn(self.scrapy,url) for url in urls]
        gevent.joinall(jobs)
        for job in jobs:
            if job.value:
                live_data=job.value.json().get('data').get('key').get('retBody').get('data').get('list')
                lottery_info=live_data[0].get('event_item').get('info')
                yield lottery_info
            else:
                self.fail_page += 1

    def process_lottery_info(self):
        for info in self.get_all_lottery_info():
            if info is not None:
                try:
                    content = info.get('lottery_info')
                    self.lottery_prize = content.get('prize').get('name')
                    self.roomid = content.get('lottery_id').split('_')[1]
                    self.platform = Config.platform
                    self.lottery_time=content.get('lottery_tm')
                    if content.get('conds')[1].get('title')==u'赠送礼物':
                        self.lottery_condition=json.dumps({"giftid": content['conds'][1]["info"]['gift_id'],"num": content['conds'][1]["info"]["num"],"prize_num": content['prize']['total']})
                    elif content.get('conds')[1].get('title')==u'发送口令':
                        self.lottery_condition = json.dumps({"command": content['conds'][1]['info']['msg'], "prize_num": content['prize']['total']})
                except Exception,e:
                    LOG.error('处理抽奖房间信息失败，msg:{}'.format(e.message))
                self.format_lottery_datas()

    def run(self):
        self.process_lottery_info()
        self.update_lottery()
        LOG.info('总共{total_page}页，失败{fail_page}页，总开播房间有{total_room}间，总共{total_lottery_room}间直播抽奖，失败{fail_lottery_room}间,耗时{times}'.format(
            total_page=self.total_page, fail_page=self.fail_page, total_lottery_room=self.total_lottery_room,total_room=self.total_room,
            fail_lottery_room=self.fail_lottery_room, times=str(time.time() - self.start_time)))


if __name__ == '__main__':
    e = EgameLottery()
    e.run()
    # e=EgameLottery()
    # #e.scrapy_single_category('2000000133')
    # start_time=time.time()
    # e.process_lottery_info()
    # #e.update_lottery()
    # print time.time()-start_time
    # print u'分类个数:',e.category_count,u'总页数:',e.total_page,u'总的房间数:',e.total_room,u'总的抽奖房间数:',e.total_lottery_room