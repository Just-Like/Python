```markdown
   对一些直播平台直播间的抽奖信息爬取：
   1、支持的平台douyu、panda、egame
   2、参与条件字段中有的事用的gitftid 这个又需要一个爬虫去爬取平台的礼物信息
   3、代码主要是用到了gevent 实现高并发爬取，加快了爬虫的爬取速度，在linux平台上运行时一个平台可以在5s内获取到所有的抽奖信息
   4、关于代理，我是将我的几台服务器用squid做出了代理服务器，只能我自己的内网中使用，有需要的可以自行修改
```
```markdown
   运行：
   1、先建立数据库heyshow_new
   2、修改config中的mysql配置，再运行db.py 文件创建表
   3、再终端下执行 python lottery_main douyu
   4、也可以运行douyu_lottery.py 文件 启动爬虫
```
   
   
