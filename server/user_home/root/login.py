#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# author：chenjianwen
# email：1071179133@qq.com
import json
from lib import read_and_write_file as rw

user_file = "./db/user.json"
user_status = False
data = rw.read(user_file)

def login(user,passwd):
    def auth(func):
        def inner(*args,**kwargs):
            global user_status
            if not user_status:
                #user = input("name：").strip()
                #passwd = input("password：").strip()
                try:
                    password =data[user]["passwd"]
                except KeyError as e:
                    exit("用户名或密码错误...")
                if data[user] and passwd == password:
                    print("[%s],welcom login ...."%user)
                    user_status = True
                else:
                    exit("用户名或密码错误...")
            if user_status:
                return func(*args,**kwargs)
        return inner
    return auth