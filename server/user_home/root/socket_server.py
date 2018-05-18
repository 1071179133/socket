#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# author：chenjianwen
# email：1071179133@qq.com

import os
import socket
#from login import login
from lib import read_and_write_file as rw

user_file = "./db/user.json"

class server_ftp(object):
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.server = socket.socket()    #声明socket类型，同时生成socket连接对象
        self.server.bind((self.host,self.port)) #绑定地址端口
        self.server.listen(5) #开始监听,最大允许5个连接排队
        print("等待连接：")

    #@login("chenjianwen","123456")
    def server_done(self):
        while True:
            data = rw.read(user_file)
            user_status = False
            conn,addr = self.server.accept()
            print("连接来了.....")
            while True:
                if not user_status:
                    user = conn.recv(102400).decode("utf-8")        #接收客户端输入的用户名
                    #conn.sendall("get user".encode("utf-8"))        #回应一下已收到用户名
                    passwd = conn.recv(102400).decode("utf-8")      #接收客户端输入的密码
                    #conn.sendall("get passwd".encode("utf-8"))      #回应一下已收到密码
                    print(user,passwd)
                    user_dir = "./%s"%user
                    if not os.path.exists(us