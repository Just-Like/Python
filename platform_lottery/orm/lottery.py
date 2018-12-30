#!/usr/bin/env python
# coding:utf-8
'''
@Auth ： Just
@File : lottery.py
@Date : 2018/8/29
'''
from sqlalchemy import Column, Integer, BigInteger, VARCHAR, TIMESTAMP, func
from config import Base
from config import CurrentConfig as Config



class Lottery(Base):
	__tablename__ = Config.lottery_table_name
	id = Column(Integer, autoincrement=True, primary_key=True, comment=u'编号')
	room_id = Column(BigInteger, nullable=False, comment=u'房间号')
	lottery_prize = Column(VARCHAR(20), nullable=False, comment=u'奖品')
	platform = Column(VARCHAR(20), nullable=False, comment=u'平台')
	lottery_time = Column(Integer(), nullable=False, comment=u'开奖时间')
	condition = Column(VARCHAR(100), nullable=False, comment=u'参与条件')
	members = Column(Integer(), default=0, comment=u'参与人数')
	create_time = Column(TIMESTAMP(True), server_default=func.now(), comment=u'创建时间')

	"""
		 create_time 本来是想用时间戳来记录的 但mysql中提供的时间戳字段貌似和其它语言中的时间戳意义不一样
		 Mysql中的timestamp格式是这样的 YYYY-MM-DD HH:MM:SS[.fraction]
		 官方文档 https://dev.mysql.com/doc/refman/8.0/en/datetime.html
		 
		 不过Mysql中提供了一个unix_timestamp()函数 当不传值的时候可以获取到当前的时间戳，不过这个不能设为
		 字段的默认值，so，自能存YYYY-MM-DD HH:MM:SS格式的create_time了
	"""

