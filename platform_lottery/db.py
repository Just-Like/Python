#!/usr/bin/env python
# coding:utf-8
'''
@Auth ： Just
@File : db.py
@Date : 2018/8/29
'''
from sqlalchemy.orm import sessionmaker
from config import Base
from orm import lottery
from sqlalchemy import create_engine,event
from sqlalchemy.exc import DisconnectionError
from config import CurrentConfig as Config

engine = create_engine(Config.DB_CONNECT_STRING.format( user=Config.mysql_user,
														password=Config.mysql_password,
														hostname=Config.mysql_hostname,
														database=Config.mysql_database,
														charset=Config.mysql_charset ), echo=Config.mysql_echo,pool_size=100)
DB_Session = sessionmaker(bind=engine)



def init_db():
	Base.metadata.create_all(engine)


def drop_db():
	Base.metadata.drop_all(engine)

def checkout_listener(dbapi_con, con_record, con_proxy):
	try:
		try:
			dbapi_con.ping(False)
		except TypeError:
			dbapi_con.ping()
	except dbapi_con.OperationalError as exc:
		if exc.args[0] in (2006, 2013, 2014, 2045, 2055):
			raise DisconnectionError()
		else:
			raise
event.listen(engine, 'checkout', checkout_listener)


if __name__ == '__main__':
	drop_db()
	init_db()