#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# author：chenjianwen
# email：1071179133@qq.com

import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import read_and_write_file as rw

databases_dir = "../db/"
databases = "../db/database.json"
log_dir = "../log/"
data = {
        "school":{},
        "teacher":{},
        "course":{},
        "classes":{},
        "student":{}
    }

if not os.path.exists(databases_dir):
    os.makedirs(databases_dir)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
if not os.path.isfile(databases):
    rw.write(data,databases)

