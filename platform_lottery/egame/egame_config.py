#!/usr/bin/env python
# coding:utf-8
'''
@Auth ： Just
@File : douyu_config.py
@Date : 2018/9/8
'''
import config
import logging
class EGConfig(config.CurrentConfig):
    """平台配置文件"""

    platform = 'egame'
    log_file='log/egame.log'

    log_level=logging.INFO
    gamelist_url='https://egame.qq.com/gamelist'  #获取所有分类

    roomlist_url='https://share.egame.qq.com/cgi-bin/pgg_live_async_fcgi?param=%7B%22key%22:%7B%22module%22:%22pgg_live_read_ifc_mt_svr%22,%22method%22:%22get_pc_live_list%22,%22param%22:%7B%22appid%22:%22{appid}%22,%22page_num%22:{pageid},%22page_size%22:40,%22tag_id%22:0,%22tag_id_str%22:%22%22%7D%7D%7D&app_info=%7B%22platform%22:4,%22terminal_type%22:2,%22egame_id%22:%22egame_official%22,%22version_code%22:%229.9.9.9%22,%22version_name%22:%229.9.9.9%22%7D&g_tk=1858969729&p_tk=&tt=1&_t={timespamt}'
    lotteryinfo_url='https://share.egame.qq.com/cgi-bin/pgg_live_async_fcgi?_t={timestamp}&g_tk=1858969729&p_tk=&param=%7B%22key%22:%7B%22module%22:%22pgg_anchor_interact_area_mt_svr%22,%22method%22:%22get_interact_area_list%22,%22param%22:%7B%22anchor_id%22:{anchor_id}%7D%7D%7D&app_info=%7B%22platform%22:4,%22terminal_type%22:2,%22egame_id%22:%22egame_official%22,%22version_code%22:%229.9.9.9%22,%22version_name%22:%229.9.9.9%22%7D&tt=1'

    crawl_frequency=250


