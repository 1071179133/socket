#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# author：chenjianwen
# email：1071179133@qq.com

import os
import logging
from logging import handlers

#创建logger
logger = logging.getLogger("marry")
logger.setLevel(logging.DEBUG)

#创建窗口handle和设置日志等级
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
#设置日志格式
ch_formatter = logging.Formatter('%(asctime)s %(name)s %(filename)s:%(lineno)d line [%(levelname)s] %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

##创建文件handler和设置日志等级为debug,设置字符编码为utf-8
log_file = os.path.join("../log/","access.log")
##通过时间截断 when='midnight'：凌晨截断；interval：时间间隔；backupCount：保留几个文件
fh = handlers.TimedRotatingFileHandler(filename=log_file,when='midnight',interval=5,backupCount=100,encoding='utf-8')
fh.setLevel(logging.DEBUG)
##设置输入文件的日志格式
fh_formatter =  logging.Formatter('%(asctime)s %(filename)s:%(lineno)d line [%(levelname)s] %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

##将日志格式添加到handler
ch.setFormatter(ch_formatter)
fh.setFormatter(fh_formatter)

##将两个handler添加进logger
logger.addHandler(ch)
logger.addHandler(fh)
