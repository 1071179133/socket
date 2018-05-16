#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# author：chenjianwen
# email：1071179133@qq.com

import os
import sys
import socket
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import read_and_write_file as rw
from lib.logger import logger

user_file = "../db/user.json"

class server_ftp(object):
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.server = socket.socket()    #声明socket类型，同时生成socket连接对象
        self.server.bind((self.host,self.port)) #绑定地址端口
        self.server.listen(5) #开始监听,最大允许5个连接排队
        logger.info("等待连接：")

    #@login("chenjianwen","123456")
    def server_done(self):
        while True:
            data = rw.read(user_file)
            user_status = False
            conn,addr = self.server.accept()
            logger.info("连接来了.....")
            while True:
                if not user_status:
                    user = conn.recv(102400).decode("utf-8")        #接收客户端输入的用户名
                    #conn.sendall("get user".encode("utf-8"))        #回应一下已收到用户名
                    passwd = conn.recv(102400).decode("utf-8")      #接收客户端输入的密码
                    #conn.sendall("get passwd".encode("utf-8"))      #回应一下已收到密码
                    print(user,passwd)
                    user_dir = "../user_home/%s"%user
                    if not os.path.exists(user_dir):            #如果登陆用户的目录不存在，则创建
                        os.makedirs(user_dir)
                    try:
                        password = data[user]["passwd"]
                    except KeyError as e:
                        exit("用户名或密码错误...")
                    if data[user] and passwd == password:           #验证账号密码是否正确
                        logger.info("user:[%s],addr:[%s],login susess...."%(user,addr))
                        user_status = True
                if user_status:
                    cmd = None
                    filename = None
                    data = None
                    cmd = conn.recv(102400).decode("utf-8")     #接收需要执行的命令
                    print(cmd)
                    if not cmd:continue
                    #conn.sendall("get cmd".encode("utf-8"))     #回应客户端已收到需要执行的命令
                    if cmd == "q":
                        logger.info("user:[%s],addr:[%s],连接断开....."%(user,addr))
                        break
                    elif "get" in cmd:
                        filename = conn.recv(102400).decode("utf-8")    #接收文件名称
                        #conn.sendall("get filename".encode("utf-8"))    #回应客户端已收到文件名称
                        logger.info("user:[%s],addr:[%s],get [%s]"%(user,addr,filename))
                        f = open("%s/%s"%(user_dir,filename),"rb")
                        f_data = f.read()
                        conn.sendall(f_data)                            #发送对应文件数据到客户端
                        logger.info("user:[%s],addr:[%s],下载文件[%s]成功" %(user,addr,filename))
                        f.close()
                    elif "push" in cmd:
                        filename = conn.recv(102400).decode("utf-8")    #若果是上传，则接收第二条数据，接收文件数据
                        conn.sendall("get filename".encode("utf-8"))    #回应客户端已收到文件名称
                        logger.info("user:[%s],addr:[%s],push [%s]"%(user,addr,filename))
                        data = conn.recv(102400)                        #接收客户端传过来的文件数据
                        f = open("%s/%s"%(user_dir,filename), 'wb')
                        f.write(data)
                        logger.info("user:[%s],addr:[%s],上传文件[%s]成功" %(user,addr,filename))
                        f.close()
                    elif "push" not in cmd and "get" not in cmd:
                        msg = os.popen("%s %s"%(cmd,user_dir)).read()
                        if msg:
                            conn.sendall(msg.encode("utf-8"))           #发送执行结果内容给客户端
                            logger.info("user:[%s],addr:[%s],执行命令[%s]" %(user,addr,cmd))
                        else:
                            conn.sendall("执行命令错误".encode("utf-8"))
                            logger.info("user:[%s],addr:[%s],执行命令出错或命令不存在，[%s]"%(user,addr,cmd))
                            continue
                    else:
                        logger.error("user:[%s],addr:[%s],不符合命令要求.....断开"%(user,addr))
                        break


