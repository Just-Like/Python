#!/usr/bin/env python
# coding:utf-8
'''
@Auth ： Just
@File : lottery.py
@Date : 2018/8/29
'''
from sqlalchemy import Column, Integer, BigInteger,VARCHAR
from db import BaseModel
from config import CurrentConfig as Config
class Lottery(BaseModel):
	__tablename__ = Config.lottery_table_name
	id=Column(Integer,autoincrement=True,primary_key=True)
	room_id = Column(BigInteger,nullable=False)
	lottery_prize=Column(VARCHAR(20),nullable=False)
	platform=Column(VARCHAR(20),nullable=False)
	lottery_time=Column(Integer(),nullable=False)
	condition=Column(VARCHAR(100),nullable=False)
	members=Column(Integer(),default=0)
	create_time=Column(Integer(),default=0)