#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# author：chenjianwen
# email：1071179133@qq.com

import os
import json

def read(filename):
    if os.path.exists(filename):    #文件是否存在
        if os.path.getsize(filename):   #文件是否为空
            f = open(filename,"r",encoding="gbk")
            data = json.loads(f.read())
            f.close()
            return data
        else:
            data = {}
            return data
    else:
        data = {}
        return data

def write(data,filename):
    f = open(filename,"w")
    json.dump(data,f,indent=4,ensure_ascii=False,sort_keys=True)
    f.close()
    return data